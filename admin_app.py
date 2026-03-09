import flet as ft
import os
import re
import sys

# Admin credentials
ADMIN_PASSWORD = "admin"  # You can change this

def get_log_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "ip_log.txt")

def main(page: ft.Page):
    page.title = "Admin Portal - Secure Login"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = "#0f172a"
    page.window_width = 1100
    page.window_height = 750
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    log_file_path = get_log_path()

    # --- Dashboard Components ---
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Timestamp", weight="bold", color="#818cf8")),
            ft.DataColumn(ft.Text("Name", weight="bold", color="#818cf8")),
            ft.DataColumn(ft.Text("IP Address", weight="bold", color="#818cf8")),
            ft.DataColumn(ft.Text("User Agent", weight="bold", color="#818cf8")),
        ],
        rows=[],
        column_spacing=20,
        expand=True,
    )

    stats_text = ft.Text("", color="#94a3b8", size=14)

    def load_logs(e=None):
        table.rows.clear()
        if not os.path.exists(log_file_path):
            stats_text.value = "Waiting for logs... (No entries yet)"
            page.update()
            return

        try:
            with open(log_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            pattern = re.compile(r"\[(.*?)\]\s*NAME:\s*(.*?)\s*\|\s*IP:\s*(.*?)\s*\|\s*UA:\s*(.*)")
            unique_ips = set()
            total_count = 0
            
            for line in reversed(lines):
                line = line.strip()
                if not line: continue
                match = pattern.search(line)
                if match:
                    timestamp, name, ip, ua = match.groups()
                    unique_ips.add(ip)
                    total_count += 1
                    ua_display = str(ua)[:60] + "..." if len(str(ua)) > 60 else str(ua)
                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(timestamp, size=12)),
                                ft.DataCell(ft.Text(name, weight="bold", selectable=True)),
                                ft.DataCell(ft.Text(ip, color="#6366f1", selectable=True)),
                                ft.DataCell(ft.Text(ua_display, size=11, color="#64748b", selectable=True)),
                            ]
                        )
                    )
            
            stats_text.value = f"Total entries: {total_count} | Unique IPs: {len(unique_ips)}"
            page.update()
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {err}"))
            page.snack_bar.open = True
            page.update()

    # --- Login View ---
    password_input = ft.TextField(
        label="Admin Password",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=12,
        border_color="#334155",
        focused_border_color="#6366f1",
        on_submit=lambda e: do_login()
    )

    login_error = ft.Text("", color=ft.Colors.RED_400, size=12)

    def do_login(e=None):
        if password_input.value == ADMIN_PASSWORD:
            show_dashboard()
        else:
            login_error.value = "Invalid password. Access denied."
            page.update()

    login_card = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.LOCK_PERSON, size=60, color="#6366f1"),
            ft.Text("Admin Login", size=24, weight="bold"),
            ft.Text("Secure area - authorization required", color="#94a3b8", size=14),
            ft.Divider(height=20, color="transparent"),
            password_input,
            login_error,
            ft.Divider(height=10, color="transparent"),
            ft.FilledButton(
                "Login to Dashboard",
                on_click=do_login,
                width=300,
                style=ft.ButtonStyle(
                    bgcolor="#6366f1",
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=40,
        bgcolor="#1e293b",
        border_radius=20,
        border=ft.border.all(1, "#334155"),
        shadow=ft.BoxShadow(blur_radius=50, spread_radius=0, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK))
    )

    # --- Navigation Logic ---
    def show_dashboard():
        page.controls.clear()
        page.padding = 30
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.title = "Visitor Intelligence Log - Admin Dashboard"
        
        header = ft.Row([
            ft.Column([
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Visitor Intelligence Log",
                            style=ft.TextStyle(
                                size=32,
                                weight="bold",
                                foreground=ft.Paint(
                                    gradient=ft.PaintLinearGradient(
                                        (0, 0), (300, 0), 
                                        [ft.Colors.INDIGO_400, ft.Colors.PURPLE_400]
                                    )
                                ),
                            ),
                        )
                    ]
                ),
                stats_text,
            ], expand=True),
            ft.FilledButton(
                "Refresh",
                icon=ft.Icons.REFRESH,
                on_click=load_logs,
                style=ft.ButtonStyle(bgcolor="#6366f1", shape=ft.RoundedRectangleBorder(radius=10))
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        page.add(
            header,
            ft.Divider(height=40, color="transparent"),
            ft.Container(
                content=ft.ListView([table], expand=True),
                padding=20,
                bgcolor="#1e293b",
                border_radius=20,
                expand=True,
                border=ft.border.all(1, "#334155")
            )
        )
        load_logs()
        page.update()

    # Start with login
    page.add(login_card)

if __name__ == "__main__":
    ft.run(main)
