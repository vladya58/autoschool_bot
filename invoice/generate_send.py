
from bs4 import BeautifulSoup
import pdfkit
import yagmail


class Generate_invoice:
    def __init__(self, input_file_path, output_file_path, a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.replacements = {'id_payment': f'{a1}', 'st_name': f'{a2}', 'user_id': f'{a3}', 'email': f'{a4}','INN': f'{a5}', 'number_phone': f'+{a6}',
                 'card': f'{a7}', 'datetime': f'{a8}', 'name_pay': f'{a9}', 'opis_pay': f'{a10}', '₽sum': f'₽{a11}', 'name_transaction': f'{a12}', 
                 '₽balance': f'₽{a13}'}
        self.generate_html()

    def generate_html(self):
        with open(self.input_file_path, 'r', encoding='utf-8') as file:
            html_code = file.read()

        soup = BeautifulSoup(html_code, 'html.parser')

        # Заменить значения атрибутов на новые значения
        for element in soup.find_all():
            for key, value in self.replacements.items():
                # Ищем совпадение внутри атрибутов элемента
                if key in element.attrs:
                    element.attrs[key] = value

                # Ищем совпадение внутри текста элемента
                elif element.string and key in element.string:
                    # Заменяем совпадение в тексте элемента
                    element.string.replace_with(element.string.replace(key, value))
                # Ищем совпадение внутри текста элемента, если он содержит переносы строк
                elif element.name == 'br' and key in str(element.next_sibling):
                    # Заменяем совпадение в тексте, находящемся после тега br
                    element.next_sibling.replace_with(str(element.next_sibling).replace(key, value))
                elif element.name == 'br' and key in str(element.next_sibling):
                    # Заменяем совпадение в тексте, находящемся после тега br
                    element.next_sibling.replace_with(str(element.next_sibling).replace(key, value))

        # Сохранить измененный HTML-код в новом файле
        with open(self.output_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(str(soup))



        
class Convert_and_send:
    def __init__(self, html_path, pdf_path, to_address):
        self.html_path = html_path
        self.pdf_path = pdf_path
        self.to_address = to_address
        self.convert_to_pdf()

    def convert_to_pdf(self):
        try:
            pdfkit.from_file(self.html_path, self.pdf_path)
        except Exception as e:
            print(f"An error occurred during PDF conversion: {e}")
            
        self.send_email()

    def send_email(self):
        # создаем объект yagmail.SMTP для отправки писем
        yag = yagmail.SMTP('autoschool058@mail.ru', 'cdjMzQQ96qt6fHnMbxss', host='smtp.mail.ru', port=465, smtp_starttls=False, smtp_ssl=True)

        # отправляем сообщение
        try:
            yag.send(
                to=self.to_address,
                subject='Кассовый чек',
                attachments=self.pdf_path,
                contents='Благодарим за транзакцию. Ваш электронный чек.'
            )
        except Exception as e:
            print(f"An error occurred during email sending: {e}")
            return False
        finally:
            yag.close()

        






# gen = Generate_invoice('test.html', 'new_example.html', replacements)
# gen.generate_pdf()