import flet as ft
import datetime

def main(page: ft.Page):
    page.title = "Formulário Completo"
    page.scroll = "adaptive"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 600
    page.window_height = 800
    
    # Variáveis para armazenar os dados
    nome = ft.Ref[ft.TextField]()
    email = ft.Ref[ft.TextField]()
    telefone = ft.Ref[ft.TextField]()
    senha = ft.Ref[ft.TextField]()
    data_nascimento = ft.Ref[ft.TextField]()
    aceita_termos = ft.Ref[ft.Checkbox]()
    sexo = ft.Ref[ft.RadioGroup]()
    satisfacao = ft.Ref[ft.Slider]()
    
    def selecionar_data(e):
        def data_selecionada(e):
            data_nascimento.current.value = (
                f"{date_picker.value.day}/{date_picker.value.month}/{date_picker.value.year}"
            )
            page.update()
            date_picker.open = False
            page.update()
        
        date_picker = ft.DatePicker(
            on_change=data_selecionada,
            first_date=datetime.datetime(1900, 1, 1),
            last_date=datetime.datetime.now(),
        )
        
        page.overlay.append(date_picker)
        page.update()
        date_picker.pick_date()
    
    def validar_email(email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def enviar_formulario(e):
        erros = []
        
        if not nome.current.value:
            erros.append("Nome é obrigatório")
            nome.current.error_text = "Campo obrigatório"
        else:
            nome.current.error_text = None
        
        if not email.current.value:
            erros.append("Email é obrigatório")
            email.current.error_text = "Campo obrigatório"
        elif not validar_email(email.current.value):
            erros.append("Email inválido")
            email.current.error_text = "Email inválido"
        else:
            email.current.error_text = None
        
        if not telefone.current.value:
            erros.append("Telefone é obrigatório")
            telefone.current.error_text = "Campo obrigatório"
        else:
            telefone.current.error_text = None
        
        if not senha.current.value:
            erros.append("Senha é obrigatória")
            senha.current.error_text = "Campo obrigatório"
        elif len(senha.current.value) < 6:
            erros.append("Senha deve ter pelo menos 6 caracteres")
            senha.current.error_text = "Mínimo 6 caracteres"
        else:
            senha.current.error_text = None
        
        if not data_nascimento.current.value:
            erros.append("Data de nascimento é obrigatória")
        
        if not sexo.current.value:
            erros.append("Sexo é obrigatório")
        
        if not aceita_termos.current.value:
            erros.append("Você deve aceitar os termos")
        
        if erros:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("\n".join(erros)),
                bgcolor=ft.colors.RED_400
            )
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Formulário enviado com sucesso!"),
                bgcolor=ft.colors.GREEN_400
            )
            page.snack_bar.open = True
            
            # Exibir dados no console (poderia ser enviado para um servidor)
            print("\nDados do Formulário:")
            print(f"Nome: {nome.current.value}")
            print(f"Email: {email.current.value}")
            print(f"Telefone: {telefone.current.value}")
            print(f"Data de Nascimento: {data_nascimento.current.value}")
            print(f"Sexo: {sexo.current.value}")
            print(f"Nível de Satisfação: {satisfacao.current.value}")
            print(f"Aceitou os termos: {aceita_termos.current.value}")
        
        page.update()
    
    form = ft.Column(
        controls=[
            ft.Text("Formulário de Cadastro", size=24, weight="bold"),
            ft.Divider(),
            
            # Campo Nome
            ft.TextField(
                ref=nome,
                label="Nome Completo",
                prefix_icon=ft.Icons.PERSON,
                border=ft.InputBorder.OUTLINE,
                hint_text="Digite seu nome completo",
                text_size=14,
            ),
            
            # Campo Email
            ft.TextField(
                ref=email,
                label="Email",
                prefix_icon=ft.Icons.EMAIL,
                border=ft.InputBorder.OUTLINE,
                hint_text="seu@email.com",
                text_size=14,
                keyboard_type=ft.KeyboardType.EMAIL,
            ),
            
            # Campo Telefone
            ft.TextField(
                ref=telefone,
                label="Telefone",
                prefix_icon=ft.Icons.PHONE,
                border=ft.InputBorder.OUTLINE,
                hint_text="(00) 00000-0000",
                text_size=14,
                keyboard_type=ft.KeyboardType.PHONE,
            ),
            
            # Campo Senha
            ft.TextField(
                ref=senha,
                label="Senha",
                prefix_icon=ft.Icons.LOCK,
                border=ft.InputBorder.OUTLINE,
                hint_text="Mínimo 6 caracteres",
                text_size=14,
                password=True,
                can_reveal_password=True,
            ),
            
            # Campo Data de Nascimento
            ft.TextField(
                ref=data_nascimento,
                label="Data de Nascimento",
                prefix_icon=ft.Icons.CALENDAR_TODAY,
                border=ft.InputBorder.OUTLINE,
                hint_text="DD/MM/AAAA",
                text_size=14,
                read_only=True
               
            ),
            
            # Campo Sexo (Radio buttons)
            ft.Text("Sexo:", size=16, weight="bold"),
            ft.RadioGroup(
                ref=sexo,
                content=ft.Column([
                    ft.Radio(value="Masculino", label="Masculino"),
                    ft.Radio(value="Feminino", label="Feminino"),
                    ft.Radio(value="Outro", label="Outro"),
                ]),
            ),
            
            # Campo Nível de Satisfação (Slider)
            ft.Text("Nível de Satisfação:", size=16, weight="bold"),
            ft.Slider(
                ref=satisfacao,
                min=0,
                max=10,
                divisions=10,
                label="{value}",
                value=5,
            ),
            
            # Checkbox Termos
            ft.Row([
                ft.Checkbox(ref=aceita_termos),
                ft.Text("Eu concordo com os termos e condições", size=14),
            ]),
            
            # Botão Enviar
            ft.ElevatedButton(
                text="ENVIAR FORMULÁRIO",
                icon=ft.Icons.SEND,
                on_click=enviar_formulario,
                style=ft.ButtonStyle(
                    padding=20,
                ),
                height=50,
            ),
        ],
        spacing=20,
    )
    
    page.add(form)

ft.app(target=main)