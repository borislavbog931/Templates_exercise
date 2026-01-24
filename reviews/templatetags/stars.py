from django import template
from django.utils.timezone import now

register = template.Library()

@register.filter
def stars(value):
    try:
        rating = float(value)
    except (ValueError, TypeError):
        return ''

    full_rating = max(int(rating),0)

    star_svg="""
        <svg class="-mt-3" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="20px" height="20px" viewBox="0 -0.5 33 33" version="1.1">
        </defs>
            <g id="Vivid.JS" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                <g id="Vivid-Icons" transform="translate(-903.000000, -411.000000)" fill="#FF6E6E">
                    <g id="Icons" transform="translate(37.000000, 169.000000)">
                        <g id="star" transform="translate(858.000000, 234.000000)">
                            <g transform="translate(7.000000, 8.000000)" id="Shape">
                                <polygon points="27.865 31.83 17.615 26.209 7.462 32.009 9.553 20.362 0.99 12.335 12.532 10.758 17.394 0 22.436 10.672 34 12.047 25.574 20.22">
        
        </polygon>
                            </g>
                        </g>
                    </g>
                </g>
            </g>
        </svg>
"""
    stars_html = star_svg * full_rating
    return stars_html