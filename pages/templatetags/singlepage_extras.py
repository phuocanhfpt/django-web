import re
from django import template
from django.template.loader import render_to_string
from products.models import Product
from bs4 import BeautifulSoup, NavigableString
import json
import html

register = template.Library()

# Cập nhật regex patterns để xử lý tốt hơn các trường hợp đặc biệt
PRODUCT_ID_PATTERN = re.compile(r'\[product\s+id\s*=\s*(\d+)\]')
PRODUCT_SLUG_PATTERN = re.compile(r'\[product\s+slug\s*=\s*["""]([\w-]+)["""]\]')
PRODUCTS_IDS_PATTERN = re.compile(r'\[products\s+ids\s*=\s*["""]([\d,\s]+)["""]\]', re.IGNORECASE)
PRODUCTS_SLUGS_PATTERN = re.compile(r'\[products\s+slugs\s*=\s*["""]([\w\-,\s]+)["""]\]', re.IGNORECASE)
PRODUCT_SLIDER_IDS_PATTERN = re.compile(r'\[product_slider\s+ids\s*=\s*["""]([\d,\s]+)["""]\]', re.IGNORECASE)
PRODUCT_SLIDER_SLUGS_PATTERN = re.compile(r'\[product_slider\s+slugs\s*=\s*["""]([\w\-,\s]+)["""]\]', re.IGNORECASE)
ACCORDION_PATTERN = re.compile(r'\[accordion\s+title\s*=\s*["""](.+?)["""]\](.*?)\[/accordion\]', re.DOTALL)
ALERT_PATTERN = re.compile(r'\[alert\s+type\s*=\s*["""]([a-z]+)["""]\](.*?)\[/alert\]', re.DOTALL)
PRICING_PATTERN = re.compile(r'\[pricing\s+title\s*=\s*["""](.+?)["""]\s+price\s*=\s*["""](.+?)["""]\s+features\s*=\s*["""](.*?)["""]\](.*?)\[/pricing\]', re.DOTALL)
GALLERY_PATTERN = re.compile(r'\[gallery\s+images\s*=\s*["""](.+?)["""]\](.*?)\[/gallery\]', re.DOTALL)
TABLE_PATTERN = re.compile(r'\[table\s+data\s*=\s*["""](.+?)["""]\](.*?)\[/table\]', re.DOTALL)
CODE_PATTERN = re.compile(r'\[code(?:\s+language\s*=\s*["\']?([\w-]+)["\']?)?\](.*?)\[/code\]', re.DOTALL | re.IGNORECASE)
QUOTE_PATTERN = re.compile(r'\[quote(?:\s+author\s*=\s*["\']?([\w\s\-\.]+)["\']?)?\](.*?)\[/quote\]', re.DOTALL | re.IGNORECASE)
CONSULTATION_FORM_PATTERN = re.compile(r'\[consultation_form\]', re.IGNORECASE)

# Helper để thay thế shortcode trong text node

def extract_shortcode_json(soup, start_marker, end_marker):
    """
    Tìm và ghép toàn bộ text giữa start_marker và end_marker, bỏ qua mọi tag HTML.
    Trả về tuple (json_text, full_html):
      - json_text: chuỗi JSON sạch
      - full_html: toàn bộ HTML của shortcode (để thay thế)
    """
    html_str = str(soup)
    start = html_str.find(start_marker)
    if start == -1:
        return None, None
    start += len(start_marker)
    end = html_str.find(end_marker, start)
    if end == -1:
        return None, None
    # Lấy toàn bộ HTML của shortcode
    full_html = html_str[html_str.rfind('[', 0, start)]
    full_html += html_str[start - len(start_marker):end + len(end_marker)]
    # Lấy phần giữa, parse lại để loại bỏ tag
    inner_html = html_str[start:end]
    inner_soup = BeautifulSoup(inner_html, 'html.parser')
    json_text = inner_soup.get_text(separator='')
    # Làm sạch entity HTML và ký tự trắng đặc biệt
    json_text = html.unescape(json_text)
    json_text = json_text.replace('\xa0', ' ').replace('\u200b', '').replace('\u202f', ' ')
    json_text = json_text.replace('\n', '').replace('\r', '').replace('\t', '')
    json_text = json_text.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#34;', '"')
    json_text = json_text.strip()
    return json_text, html_str[html_str.rfind('[', 0, start):end + len(end_marker)]

def replace_shortcodes_in_text(text):
    # Thay thế các dạng quote khác nhau thành dạng chuẩn
    text = text.replace('&quot;', '"').replace('"', '"').replace('"', '"')
    
    # Parse HTML để xử lý các trường hợp bị chèn tag
    soup = BeautifulSoup(text, 'html.parser')
    html = str(soup)

    # Xử lý gallery
    while '[gallery images=' in html:
        json_text, full_html = extract_shortcode_json(soup, "[gallery images='", "']")
        if not json_text or not full_html:
            break
        try:
            images_data = json.loads(json_text)
            rendered = render_to_string('pages/_gallery.html', {'images': images_data})
        except Exception as e:
            rendered = f'<div class="alert alert-danger">Lỗi định dạng gallery: {e}</div>'
        html = html.replace(full_html, rendered, 1)
        soup = BeautifulSoup(html, 'html.parser')

    # Xử lý table
    while '[table data=' in html:
        json_text, full_html = extract_shortcode_json(soup, "[table data='", "']")
        if not json_text or not full_html:
            break
        try:
            table_data = json.loads(json_text)
            header = table_data.get('header', [])
            rows = table_data.get('rows', [])
            rendered = render_to_string('pages/_table.html', {'header': header, 'rows': rows})
        except Exception as e:
            rendered = f'<div class="alert alert-danger">Lỗi định dạng bảng: {e}</div>'
        html = html.replace(full_html, rendered, 1)
        soup = BeautifulSoup(html, 'html.parser')

    # Sau khi xử lý gallery/table, tiếp tục các shortcode khác như cũ
    text = html

    # Accordion
    def replace_accordion(match):
        title = match.group(1).strip()
        content = match.group(2).strip()
        return render_to_string('pages/_accordion.html', {'title': title, 'content': content})
    text = ACCORDION_PATTERN.sub(replace_accordion, text)

    # Alert
    def replace_alert(match):
        alert_type = match.group(1).strip()
        content = match.group(2).strip()
        return render_to_string('pages/_alert.html', {'type': alert_type, 'content': content})
    text = ALERT_PATTERN.sub(replace_alert, text)

    # Pricing
    def replace_pricing(match):
        title = match.group(1).strip()
        price = match.group(2).strip()
        features = [f.strip() for f in match.group(3).split(';') if f.strip()]
        content = match.group(4).strip()
        return render_to_string('pages/_pricing.html', {'title': title, 'price': price, 'features': features, 'content': content})
    text = PRICING_PATTERN.sub(replace_pricing, text)

    # [products ids="1,2,3"]
    def replace_ids(match):
        ids = [i.strip() for i in match.group(1).split(',') if i.strip()]
        products = Product.objects.filter(id__in=ids, status=True)
        if products.exists():
            return render_to_string('products/_product_cards_list.html', {'products': products})
        return '<div class="alert alert-warning">Không tìm thấy sản phẩm nào.</div>'
    text = PRODUCTS_IDS_PATTERN.sub(replace_ids, text)

    # [products slugs="slug-1,slug-2"]
    def replace_slugs(match):
        slugs = [s.strip() for s in match.group(1).split(',') if s.strip()]
        products = Product.objects.filter(slug__in=slugs, status=True)
        if products.exists():
            return render_to_string('products/_product_cards_list.html', {'products': products})
        return '<div class="alert alert-warning">Không tìm thấy sản phẩm nào.</div>'
    text = PRODUCTS_SLUGS_PATTERN.sub(replace_slugs, text)

    # [product_slider ids="1,2,3"]
    def replace_slider_ids(match):
        ids = [i.strip() for i in match.group(1).split(',') if i.strip()]
        products = Product.objects.filter(id__in=ids, status=True)
        if products.exists():
            return render_to_string('products/_product_slider.html', {'products': products})
        return '<div class="alert alert-warning">Không tìm thấy sản phẩm nào cho slider.</div>'
    text = PRODUCT_SLIDER_IDS_PATTERN.sub(replace_slider_ids, text)

    # [product_slider slugs="slug-1,slug-2"]
    def replace_slider_slugs(match):
        slugs = [s.strip() for s in match.group(1).split(',') if s.strip()]
        products = Product.objects.filter(slug__in=slugs, status=True)
        if products.exists():
            return render_to_string('products/_product_slider.html', {'products': products})
        return '<div class="alert alert-warning">Không tìm thấy sản phẩm nào cho slider.</div>'
    text = PRODUCT_SLIDER_SLUGS_PATTERN.sub(replace_slider_slugs, text)

    # [product id=123]
    def replace_id(match):
        product_id = match.group(1).strip()
        try:
            product = Product.objects.get(id=product_id, status=True)
            return render_to_string('products/_product_card.html', {'product': product})
        except Product.DoesNotExist:
            return f'<div class="alert alert-warning">Sản phẩm không tồn tại (id={product_id})</div>'
    text = PRODUCT_ID_PATTERN.sub(replace_id, text)

    # [product slug="abc"]
    def replace_slug(match):
        slug = match.group(1).strip()
        try:
            product = Product.objects.get(slug=slug, status=True)
            return render_to_string('products/_product_card.html', {'product': product})
        except Product.DoesNotExist:
            return f'<div class="alert alert-warning">Sản phẩm không tồn tại (slug={slug})</div>'
    text = PRODUCT_SLUG_PATTERN.sub(replace_slug, text)

    # CODE
    def replace_code(match):
        language = match.group(1) or 'text'
        code_content = match.group(2).strip()
        return render_to_string('pages/_code.html', {'language': language, 'code': code_content})
    text = CODE_PATTERN.sub(replace_code, text)

    # QUOTE
    def replace_quote(match):
        author = match.group(1)
        quote_content = match.group(2).strip()
        return render_to_string('pages/_quote.html', {'author': author, 'quote': quote_content})
    text = QUOTE_PATTERN.sub(replace_quote, text)

    # CONSULTATION FORM
    def replace_consultation_form(match):
        return render_to_string('pages/_consultation_form.html')
    text = CONSULTATION_FORM_PATTERN.sub(replace_consultation_form, text)

    return text

@register.filter
def render_shortcodes(content):
    if not content:
        return ''
        
    # Parse HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Lấy toàn bộ HTML dưới dạng string
    html = str(soup)
    
    # Thay thế shortcode trên toàn bộ HTML
    html = replace_shortcodes_in_text(html)
    
    # Parse lại HTML đã thay thế
    soup = BeautifulSoup(html, 'html.parser')

    # Gom các node lạc vào sau .accordion-item vào trong .accordion-body gần nhất
    for acc_item in soup.find_all('div', class_='accordion-item'):
        acc_body = acc_item.find('div', class_='accordion-body')
        if not acc_body:
            continue
        # Gom tất cả các node kế tiếp (sibling) cho đến khi gặp .accordion-item mới hoặc hết node
        nodes_to_move = []
        next_node = acc_item.next_sibling
        while next_node:
            # Bỏ qua node chỉ là khoảng trắng
            if isinstance(next_node, NavigableString) and not next_node.strip():
                temp = next_node
                next_node = next_node.next_sibling
                temp.extract()
                continue
            # Nếu là .accordion-item mới thì dừng
            if getattr(next_node, 'name', None) == 'div' and 'accordion-item' in (next_node.get('class') or []):
                break
            # Gom node này
            nodes_to_move.append(next_node)
            next_node = next_node.next_sibling
        # Chuyển các node gom được vào acc_body
        for node in nodes_to_move:
            acc_body.append(node.extract() if hasattr(node, 'extract') else node)

    return str(soup) 