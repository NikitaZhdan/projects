import flet as ft
import sqlite3


def main(page: ft.Page):
    page.title = 'Библиотека'
    page.window_width = 600
    page.window_height = 700
    page.update()

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    def show_books(e):
        db = sqlite3.connect('Books')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Book")
        res = cursor.fetchall()
        if res is not None:
            for book in res:
                tasks_view.controls.append(ft.Row([
                    ft.Text(f'{book[0]}: {book[1]} - "{book[2]}".'),
                ], alignment=ft.MainAxisAlignment.START)
                )

        db.commit()
        db.close()
        view.update()

    def add_clicked(e):
        db = sqlite3.connect('Books')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Book (
                                    Number INTEGER PRIMARY KEY,
                                    Author TEXT UNIQUE, 
                                    Book TEXT
                           )""")

        author, book = new_task.value.split('-')
        cursor.execute(F"INSERT INTO Book VALUES(NULL,'{author}','{book}')")
        new_task.value = ""
        db.commit()
        db.close()
        view.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.API),
        leading_width=40,
        title=ft.Text("Список книг"),
        center_title=False,
        bgcolor=ft.colors.LIGHT_BLUE,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=change_theme),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Книги"),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(
                        text="Показать книги",
                        checked=False,
                        on_click=show_books
                    ),
                ]
            ),
        ],
    )
    new_task = ft.TextField(hint_text="Добавить книгу", expand=True)
    tasks_view = ft.Column()
    view = ft.Column(
        width=600,
        controls=[
            ft.Row(
                controls=[
                    new_task,
                    ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked),
                    ft.FloatingActionButton(icon=ft.icons.BOOK, on_click=show_books)
                ],
            ),
            tasks_view,
        ],
    )
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(view)
    page.update()


ft.app(target=main)
