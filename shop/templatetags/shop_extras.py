from django import template

register = template.Library()


@register.filter
def rupees(value):
    """1499 -> ₹1,499 (Indian digit grouping)."""
    s = str(int(value or 0))
    if len(s) > 3:
        head, tail, groups = s[:-3], s[-3:], []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        s = ",".join(groups) + "," + tail
    return "₹" + s
