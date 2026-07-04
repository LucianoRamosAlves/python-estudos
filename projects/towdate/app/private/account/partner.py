from datetime import date, datetime

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.extensions import db
from app.forms.partner_forms import PartnerConnectForm, PartnerDisconnectForm
from app.models.relationship import Relationship
from app.models.relationship_member import RelationshipMember
from app.models.user import User

from app.private.routes import private


INVITE_CODE_MAX_AGE_SECONDS = 60 * 60 * 24 * 7


def obter_membro_relacionamento_ativo(user):
    membros = sorted(
        user.relationships,
        key=lambda member: member.joined_at or datetime.min,
        reverse=True,
    )

    for member in membros:
        if member.relationship and member.relationship.relationship_is_active:
            return member

    return None


def obter_parceiro_conectado(user):
    member = obter_membro_relacionamento_ativo(user)
    if member is None:
        return None, None

    for relationship_member in member.relationship.members:
        if relationship_member.user_id != user.id:
            return relationship_member.user, relationship_member

    return None, member


def obter_serializador_convite():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        salt="partner-invite-code",
    )


def gerar_codigo_convite(user):
    return obter_serializador_convite().dumps({"user_id": user.id})


def validar_codigo_convite(code):
    try:
        payload = obter_serializador_convite().loads(
            code,
            max_age=INVITE_CODE_MAX_AGE_SECONDS,
        )
    except SignatureExpired:
        return None, "Este código de convite expirou. Gere um novo código."
    except BadSignature:
        return None, "Código de convite inválido."

    user_id = payload.get("user_id")
    if not user_id:
        return None, "Código de convite inválido."

    target_user = db.session.get(User, int(user_id))
    if target_user is None:
        return None, "Não foi possível localizar o usuário deste convite."

    return target_user, None


def formatar_data_ptbr(value):
    if value is None:
        return None

    months = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro",
    }

    raw_date = value.date() if isinstance(value, datetime) else value
    return f"{raw_date.day} de {months[raw_date.month]} de {raw_date.year}"


def criar_relacionamento_base():
    relationship = Relationship(
        relationship_status="namorando",
        relationship_start_date=date.today(),
    )
    db.session.add(relationship)
    db.session.flush()
    return relationship


def conectar_parceiro(current_user, partner_user):
    current_partner, current_member = obter_parceiro_conectado(current_user)
    if current_partner is not None:
        return "Você já possui um parceiro conectado."

    if partner_user.id == current_user.id:
        return "Você não pode conectar a própria conta."

    partner_partner, partner_member = obter_parceiro_conectado(partner_user)
    if partner_partner is not None:
        return "Este usuário já possui um parceiro conectado."

    if partner_member is not None:
        return "Este usuário já participa de um relacionamento e não pode ser conectado sem perder dados existentes."

    relationship = current_member.relationship if current_member is not None else criar_relacionamento_base()

    if current_member is None:
        db.session.add(
            RelationshipMember(
                relationship_id=relationship.id,
                user_id=current_user.id,
            )
        )

    db.session.add(
        RelationshipMember(
            relationship_id=relationship.id,
            user_id=partner_user.id,
        )
    )
    db.session.commit()

    return None


def desconectar_parceiro(user):
    partner, partner_member = obter_parceiro_conectado(user)
    if partner is None or partner_member is None or partner_member.user_id == user.id:
        return False

    db.session.delete(partner_member)
    db.session.commit()
    return True


def montar_contexto_parceiro(connect_form=None, disconnect_form=None):
    partner, partner_member = obter_parceiro_conectado(current_user)
    is_connected = partner is not None
    relationship_member = obter_membro_relacionamento_ativo(current_user)
    relationship = relationship_member.relationship if relationship_member else None
    connected_since_source = None

    if is_connected and partner_member is not None:
        if partner_member.joined_at is not None:
            connected_since_source = partner_member.joined_at
        elif relationship is not None:
            connected_since_source = relationship.created_at

    return {
        "active_page": "partner",
        "connect_form": connect_form or PartnerConnectForm(),
        "disconnect_form": disconnect_form or PartnerDisconnectForm(),
        "current_user_name": current_user.first_name,
        "partner_name": partner.full_name if partner else None,
        "partner_avatar": partner.avatar if partner else None,
        "partner_status": "connected" if is_connected else "disconnected",
        "pending_request": False,
        "invite_code": gerar_codigo_convite(current_user),
        "connected_since": formatar_data_ptbr(connected_since_source),
        "is_connected": is_connected,
        "can_connect": not is_connected,
    }


@private.route("/account/partner", methods=["GET", "POST"])
@login_required
def account_partner():
    connect_form = PartnerConnectForm()
    disconnect_form = PartnerDisconnectForm()
    form_type = request.form.get("form_type")

    if request.method == "POST":
        if form_type == "connect_partner":
            if not connect_form.validate_on_submit():
                flash("Corrija o código de convite informado.", "error")
                return render_template(
                    "private/accounts/partner.html",
                    **montar_contexto_parceiro(connect_form, disconnect_form),
                )

            partner_user, invite_error = validar_codigo_convite(connect_form.partner_code.data.strip())
            if invite_error:
                connect_form.partner_code.errors.append(invite_error)
                flash(invite_error, "error")
                return render_template(
                    "private/accounts/partner.html",
                    **montar_contexto_parceiro(connect_form, disconnect_form),
                )

            connection_error = conectar_parceiro(current_user, partner_user)
            if connection_error:
                connect_form.partner_code.errors.append(connection_error)
                flash(connection_error, "error")
                return render_template(
                    "private/accounts/partner.html",
                    **montar_contexto_parceiro(connect_form, disconnect_form),
                )

            flash("Parceiro conectado com sucesso!", "success")
            return redirect(url_for("private.account_partner"))

        if form_type == "disconnect_partner":
            if not disconnect_form.validate_on_submit():
                flash("Não foi possível validar a solicitação de desconexão.", "error")
                return render_template(
                    "private/accounts/partner.html",
                    **montar_contexto_parceiro(connect_form, disconnect_form),
                )

            if not desconectar_parceiro(current_user):
                flash("Nenhum parceiro conectado para desconectar.", "warning")
                return redirect(url_for("private.account_partner"))

            flash("Parceiro desconectado com sucesso.", "success")
            return redirect(url_for("private.account_partner"))

    return render_template(
        "private/accounts/partner.html",
        **montar_contexto_parceiro(connect_form, disconnect_form),
    )
