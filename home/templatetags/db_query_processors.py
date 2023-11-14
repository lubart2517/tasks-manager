from django import template

register = template.Library()


@register.filter
def round_completion(completed_tasks, all_tasks) -> int:
    return int(round(completed_tasks/all_tasks/5.0 * 100, 0)*5.0)
