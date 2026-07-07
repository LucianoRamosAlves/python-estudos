from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.goal_forms import GoalFilterForm, GoalForm, GoalProgressForm
from app.private.routes import private
from app.services.goal_service import (
    GoalServiceError,
    complete_goal_for_user,
    create_goal_for_user,
    delete_goal_for_user,
    get_goal_for_user,
    get_goals_for_user,
    update_goal_for_user,
    update_goal_progress_for_user,
)


def _first_form_error(form):
    for errors in form.errors.values():
        if errors:
            return errors[0]
    return "Não foi possível validar a meta."


@private.route("/metas", methods=["GET", "POST"])
@login_required
def metas():
    form = GoalForm()
    filter_form = GoalFilterForm(request.args)

    if form.validate_on_submit():
        try:
            create_goal_for_user(current_user, form)
            flash("Meta criada com sucesso!", "success")
            return redirect(url_for("private.metas"))
        except GoalServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("private.metas"))

    if form.is_submitted():
        flash(_first_form_error(form), "error")
        return redirect(url_for("private.metas"))

    goals = get_goals_for_user(
        current_user,
        category=filter_form.category.data or None,
        status=filter_form.status.data or None,
        sort_by=filter_form.sort_by.data or "priority",
        sort_order=filter_form.order.data or "desc",
    )

    progress_form = GoalProgressForm()

    return render_template(
        "private/metas/metas.html",
        form=form,
        filter_form=filter_form,
        progress_form=progress_form,
        goals=goals,
    )


@private.route("/metas/<int:goal_id>/editar", methods=["GET", "POST"])
@login_required
def editar_meta(goal_id):
    goal = get_goal_for_user(current_user, goal_id)
    if goal is None:
        flash("Meta não encontrada.", "error")
        return redirect(url_for("private.metas"))

    form = GoalForm()

    if form.validate_on_submit():
        try:
            update_goal_for_user(current_user, goal_id, form)
            flash("Meta atualizada com sucesso!", "success")
            return redirect(url_for("private.metas"))
        except GoalServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("private.editar_meta", goal_id=goal_id))

    if form.is_submitted():
        flash(_first_form_error(form), "error")

    if request.method == "GET":
        form.title.data = goal.title
        form.description.data = goal.description
        form.category.data = goal.category
        form.priority.data = goal.priority
        form.status.data = goal.status
        form.progress.data = goal.progress
        form.target_date.data = goal.target_date
        form.favorite.data = goal.favorite

    return render_template(
        "private/metas/editar_meta.html",
        form=form,
        goal=goal,
    )


@private.route("/metas/<int:goal_id>/excluir", methods=["POST"])
@login_required
def excluir_meta(goal_id):
    try:
        delete_goal_for_user(current_user, goal_id)
        flash("Meta excluída com sucesso.", "success")
    except GoalServiceError as error:
        flash(str(error), "error")

    return redirect(request.referrer or url_for("private.metas"))


@private.route("/metas/<int:goal_id>/concluir", methods=["POST"])
@login_required
def concluir_meta(goal_id):
    try:
        complete_goal_for_user(current_user, goal_id)
        flash("Meta concluída com sucesso.", "success")
    except GoalServiceError as error:
        flash(str(error), "error")

    return redirect(request.referrer or url_for("private.metas"))


@private.route("/metas/<int:goal_id>/progresso", methods=["POST"])
@login_required
def atualizar_progresso_meta(goal_id):
    form = GoalProgressForm()
    if form.validate_on_submit():
        try:
            update_goal_progress_for_user(current_user, goal_id, form.progress.data)
            flash("Progresso atualizado com sucesso.", "success")
        except GoalServiceError as error:
            flash(str(error), "error")
    else:
        flash(_first_form_error(form), "error")

    return redirect(request.referrer or url_for("private.metas"))
