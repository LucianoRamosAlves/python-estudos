from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.calendar_forms import CalendarEventForm
from app.private.routes import private
from app.services.calendar_service import (
    CalendarServiceError,
    build_calendar_context,
    create_event_for_relationship,
    delete_event_for_relationship,
    get_event_for_relationship,
    update_event_for_relationship,
)


def _first_form_error(form):
    for errors in form.errors.values():
        if errors:
            return errors[0]
    return "Não foi possível validar o evento."


@private.route("/calendario", methods=["GET", "POST"])
@login_required
def calendario():
    form = CalendarEventForm()

    if form.validate_on_submit():
        try:
            create_event_for_relationship(current_user, form)
            flash("Evento criado com sucesso!", "success")
            return redirect(url_for("private.calendario"))
        except CalendarServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("private.calendario"))

    if form.is_submitted():
        flash(_first_form_error(form), "error")
        return redirect(url_for("private.calendario"))

    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)
    context = build_calendar_context(current_user, year=year, month=month)

    return render_template(
        "private/calendario/calendario.html",
        form=form,
        calendar=context,
    )


@private.route("/calendario/<int:event_id>/editar", methods=["GET", "POST"])
@login_required
def editar_evento(event_id):
    event = get_event_for_relationship(current_user, event_id)
    if event is None:
        flash("Evento não encontrado.", "error")
        return redirect(url_for("private.calendario"))

    form = CalendarEventForm()

    if form.validate_on_submit():
        try:
            update_event_for_relationship(current_user, event_id, form)
            flash("Evento atualizado com sucesso!", "success")
            return redirect(url_for("private.calendario"))
        except CalendarServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("private.editar_evento", event_id=event_id))

    if form.is_submitted():
        flash(_first_form_error(form), "error")

    if request.method == "GET":
        form.title.data = event.title
        form.description.data = event.description
        form.event_date.data = event.event_date
        form.event_time.data = event.event_time
        form.location.data = event.location
        form.category.data = event.category
        form.favorite.data = event.favorite

    return render_template(
        "private/calendario/editar_evento.html",
        form=form,
        event=event,
    )


@private.route("/calendario/<int:event_id>/excluir", methods=["POST"])
@login_required
def excluir_evento(event_id):
    try:
        delete_event_for_relationship(current_user, event_id)
        flash("Evento excluído com sucesso.", "success")
    except CalendarServiceError as error:
        flash(str(error), "error")

    return redirect(request.referrer or url_for("private.calendario"))
