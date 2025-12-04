import io
import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

# Importar módulos del proyecto
try:
    from lexer import Lexer
    from mi_parser import Parser, NodoPrograma
    from semantico import AnalizadorSemantico
    from interprete import Interprete
except Exception as e:
    print("ERROR importando módulos del proyecto:", e)
    raise


class CompiladorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compilador - Interfaz gráfica")
        self.geometry("1100x700")

        self._create_widgets()
        self.current_file = None

    def _create_widgets(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(paned, width=520)
        right_frame = ttk.Frame(paned, width=560)
        paned.add(left_frame, weight=1)
        paned.add(right_frame, weight=1)

        toolbar = ttk.Frame(left_frame)
        toolbar.pack(fill=tk.X, padx=4, pady=4)

        btn_run = ttk.Button(toolbar, text="Ejecutar", command=self.run_all)
        btn_run.pack(side=tk.LEFT, padx=6)

        editor_frame = ttk.Frame(left_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 4))

        self.editor = ScrolledText(editor_frame, wrap=tk.NONE, undo=True)
        self.editor.pack(fill=tk.BOTH, expand=True)
        self.editor.insert("1.0", "// Escribe tu código aquí\n")

        # --- Pestañas derechas ---
        self.tab_control = ttk.Notebook(right_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Léxico
        self.tab_tokens = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_tokens, text="Léxico")

        self.tokens_list = ttk.Treeview(
            self.tab_tokens, columns=("tipo", "valor"), show='headings', height=12
        )
        self.tokens_list.heading("tipo", text="Tipo")
        self.tokens_list.heading("valor", text="Valor")
        self.tokens_list.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.lex_errors = ScrolledText(self.tab_tokens, height=6)
        self.lex_errors.pack(fill=tk.X, padx=4, pady=4)

        # Sintáctico
        self.tab_sint = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_sint, text="Sintáctico")

        sint_pane = ttk.PanedWindow(self.tab_sint, orient=tk.VERTICAL)
        sint_pane.pack(fill=tk.BOTH, expand=True)

        self.ast_tree = ttk.Treeview(sint_pane)
        sint_pane.add(self.ast_tree, weight=3)

        self.parse_errors = ScrolledText(sint_pane, height=6)
        sint_pane.add(self.parse_errors, weight=1)

        # Semántico
        self.tab_sem = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_sem, text="Semántico")

        self.sem_table = ttk.Treeview(
            self.tab_sem, columns=("nombre", "tipo", "usada"), show='headings'
        )
        self.sem_table.heading("nombre", text="Nombre")
        self.sem_table.heading("tipo", text="Tipo")
        self.sem_table.heading("usada", text="Usada")
        self.sem_table.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.sem_errors = ScrolledText(self.tab_sem, height=6)
        self.sem_errors.pack(fill=tk.X, padx=4, pady=4)

        # Consola
        self.tab_out = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_out, text="Salida")

        self.console = ScrolledText(self.tab_out, height=12)
        self.console.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    # -------- ARCHIVOS ----------
    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("BZ files", "*.bz"), ("All files", "*.*")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", text)
        self.current_file = path
        self.title(f"Compilador - {os.path.basename(path)}")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", tk.END))
            messagebox.showinfo("Guardar", "Archivo guardado correctamente")
        else:
            self.save_file_as()

    def save_file_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".bz",
            filetypes=[("BZ files", "*.bz"), ("All files", "*.*")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0", tk.END))
        self.current_file = path
        self.title(f"Compilador - {os.path.basename(path)}")
        messagebox.showinfo("Guardar", "Archivo guardado correctamente")

    # -------- ETAPAS DEL COMPILADOR ----------
    def select_tab(self, index: int):
        """Corrección: ahora sí encuentra directamente el Notebook."""
        try:
            self.tab_control.select(index)
        except Exception:
            pass

    def run_all(self):
        # Ejecutar etapas por orden y detenerse si hay errores
        self.run_lexico()
        # Si hay errores léxicos, mostrar en la pestaña de Salida y no continuar
        if getattr(self, '_last_lex_errors', None):
            self.console.insert(tk.END, "[Salida] Errores léxicos detectados:\n")
            for e in self._last_lex_errors:
                self.console.insert(tk.END, e + "\n")
            self.console.see(tk.END)
            self.select_tab(3)
            return

        self.run_parser()
        # Si hay errores sintácticos, mostrar en la pestaña de Salida y no continuar
        if getattr(self, '_last_parse_errors', None):
            self.console.insert(tk.END, "[Salida] Errores sintácticos detectados:\n")
            for e in self._last_parse_errors:
                self.console.insert(tk.END, e + "\n")
            self.console.see(tk.END)
            self.select_tab(3)
            return

        self.run_semantico()
        # Si hay errores semánticos, mostrar en la pestaña de Salida y no ejecutar
        if getattr(self, '_last_semantic_errors', None):
            self.console.insert(tk.END, "[Salida] Errores semánticos detectados:\n")
            for e in self._last_semantic_errors:
                self.console.insert(tk.END, e + "\n")
            self.console.see(tk.END)
            self.select_tab(3)
            return

        # Si todo ok, ejecutar intérprete
        self.run_interprete()

    # ------ LÉXICO ------
    def run_lexico(self):
        code = self.editor.get("1.0", tk.END)
        lexer = Lexer(code)
        tokens, errores = lexer.analizar()

        self.tokens_list.delete(*self.tokens_list.get_children())
        self.lex_errors.delete("1.0", tk.END)

        # Guardar errores léxicos para control de flujo
        self._last_lex_errors = errores

        for t in tokens:
            tipo = getattr(t, "tipo", repr(t))
            valor = getattr(t, "valor", "")
            self.tokens_list.insert("", tk.END, values=(tipo, valor))

        if errores:
            for e in errores:
                self.lex_errors.insert(tk.END, e + "\n")
            # Mostrar errores en consola de salida también (resumen)
            self.console.insert(tk.END, "[Léxico] Errores:\n")
            for e in errores:
                self.console.insert(tk.END, e + "\n")
        else:
            self.lex_errors.insert("end", "Sin errores léxicos ✔\n")

        self.console.insert(tk.END, f"[Léxico] Tokens: {len(tokens)}  Errores: {len(errores)}\n")
        self.console.see(tk.END)

        self._last_tokens = tokens

    # ------ PARSER ------
    def run_parser(self):
        if not hasattr(self, "_last_tokens"):
            self.run_lexico()

        tokens = self._last_tokens
        parser = Parser(tokens)
        ast = parser.parse()

        self.ast_tree.delete(*self.ast_tree.get_children())
        self.parse_errors.delete("1.0", tk.END)

        # Guardar errores sintácticos para control de flujo
        self._last_parse_errors = parser.errores

        if parser.errores:
            for e in parser.errores:
                self.parse_errors.insert(tk.END, e + "\n")
            # Mostrar resumen en la consola de salida
            self.console.insert(tk.END, "[Sintáctico] Errores:\n")
            for e in parser.errores:
                self.console.insert(tk.END, e + "\n")
        else:
            self.parse_errors.insert(tk.END, "Sin errores sintácticos ✔\n")

        # TreeView recursivo
        def insertar_nodo(tree, parent, nodo):
            text = type(nodo).__name__
            for campo in ("nombre", "valor"):
                if hasattr(nodo, campo):
                    text += f" - {getattr(nodo, campo)}"
            node_id = tree.insert(parent, tk.END, text=text)

            # Evitar duplicados en atributos
            attrs = ["sentencias", "izquierda", "derecha", "expresion", "tipo"]
            for attr in attrs:
                if hasattr(nodo, attr):
                    val = getattr(nodo, attr)
                    if isinstance(val, list):
                        for item in val:
                            insertar_nodo(tree, node_id, item)
                    elif isinstance(val, (int, str)):
                        tree.insert(node_id, tk.END, text=f"{attr}: {val}")
                    elif val is not None:
                        insertar_nodo(tree, node_id, val)

        if isinstance(ast, NodoPrograma):
            insertar_nodo(self.ast_tree, '', ast)

        self.console.insert(tk.END, "[Sintáctico] Análisis completado\n")
        self.console.see(tk.END)

        self._last_ast = ast

    # ------ SEMÁNTICO ------
    def run_semantico(self):
        if not hasattr(self, "_last_ast"):
            self.run_parser()

        ast = self._last_ast
        analizador = AnalizadorSemantico()

        old_stdout = sys.stdout
        sio = io.StringIO()
        sys.stdout = sio
        resultado = analizador.analizar(ast)
        sys.stdout = old_stdout
        tabla_impresion = sio.getvalue()

        self.sem_table.delete(*self.sem_table.get_children())
        self.sem_errors.delete("1.0", tk.END)

        # Guardar errores semánticos para control de flujo
        self._last_semantic_errors = analizador.errores

        if analizador.errores:
            for e in analizador.errores:
                self.sem_errors.insert(tk.END, e + "\n")
            # Mostrar resumen en la consola de salida
            self.console.insert(tk.END, "[Semántico] Errores:\n")
            for e in analizador.errores:
                self.console.insert(tk.END, e + "\n")
        else:
            self.sem_errors.insert(tk.END, "Sin errores semánticos ✔\n")

        try:
            tabla = analizador.obtener_tabla()
            if hasattr(tabla, "tabla"):
                for simb in tabla.tabla:
                    try:
                        self.sem_table.insert(
                            "", tk.END,
                            values=(
                                simb.nombre,
                                getattr(simb, "tipo", ""),
                                getattr(simb, "usada", False)
                            )
                        )
                    except Exception:
                        pass
        except Exception:
            pass

        if tabla_impresion.strip():
            self.console.insert(tk.END, "[Semántico]\n" + tabla_impresion + "\n")

        self.console.insert(tk.END, f"[Semántico] Resultado: {'OK' if resultado else 'FALLÓ'}\n")
        self.console.see(tk.END)

        self._last_semantic_ok = bool(resultado)
        self._last_analizador = analizador

    # ------ INTÉRPRETE ------
    def run_interprete(self):
        if not getattr(self, "_last_semantic_ok", False):
            self.run_semantico()
            if not getattr(self, "_last_semantic_ok", False):
                self.console.insert(tk.END, "[Intérprete] No se puede ejecutar por errores semánticos\n")
                return

        ast = self._last_ast
        analizador = self._last_analizador

        try:
            tabla = analizador.obtener_tabla()
        except Exception:
            tabla = None

        interprete = Interprete(tabla)

        old_stdout = sys.stdout
        sio = io.StringIO()
        sys.stdout = sio

        try:
            interprete.ejecutar(ast)
        except Exception as e:
            sys.stdout = old_stdout
            self.console.insert(tk.END, f"[Intérprete] Error: {e}\n")
            return

        sys.stdout = old_stdout
        salida = sio.getvalue()

        self.console.insert(tk.END, "[Ejecución]\n" + salida + "\n")
        self.console.see(tk.END)


if __name__ == '__main__':
    app = CompiladorGUI()
    app.mainloop()
