import tkinter as tk
from tkinter import font
from tkinter import ttk, filedialog, scrolledtext, messagebox
import lexer

class LOLCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TL?DR CMSC 124 Project")
        self.root.geometry("1200x700")
        
        # variables to store program state
        self.tokens = []
        self.symbol_table = {}
        self.current_file = None
        
        # vscode dark theme colors 
        bg_color = "#1e1e1e"      
        frame_color = "#252526"   
        text_bg = "#1e1e1e"       
        text_fg = "#d4d4d4"     
        accent_blue = "#007acc"   
        button_fg = "#ffffff"     
        console_bg = "#1e1e1e"    
        console_fg = "#00ff00"    
        
        # create main container
        main_container = tk.Frame(root, bg=bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # paned window for resizable containers
        paned_window = tk.PanedWindow(main_container, orient=tk.VERTICAL, 
                                      bg=bg_color, sashwidth=5, 
                                      sashrelief=tk.RAISED, bd=0)
        paned_window.pack(fill=tk.BOTH, expand=True)
        #------------------------------------------------------------------------------------------------------------
        # top container (file explorer + text editor + lexemes + symbol table)
        top_pane = tk.Frame(paned_window, bg=bg_color)
        paned_window.add(top_pane, minsize=300)
        
        # create top section (file explorer + text editor)
        top_section = tk.Frame(top_pane, bg=bg_color)
        top_section.pack(fill=tk.BOTH, expand=True)
        #------------------------------------------------------------------------------------------------------------
        # left side
        left_panel = tk.Frame(top_section, bg=bg_color)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # file explorer section
        file_frame = tk.LabelFrame(left_panel, text="File Explorer", 
                                   font=("Helvetica", 10, "bold"), bg=frame_color, fg=text_fg, padx=5, pady=5)
        file_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(file_frame, text="Open File", command=self.open_file,
                 bg=accent_blue, fg=button_fg, font=("Helvetica", 9, "bold"),
                 cursor="hand2", padx=10, activebackground="#005a9e", activeforeground="white").pack(side=tk.LEFT, padx=5)
        
        self.file_label = tk.Label(file_frame, text="No file selected", 
                                   bg=frame_color, fg=text_fg, anchor="w")
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # text editor section
        editor_frame = tk.LabelFrame(left_panel, text="Text Editor", 
                                     font=("Helvetica", 10, "bold"), bg=frame_color, fg=text_fg)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        # inner container for the execute button + text area
        editor_inner = tk.Frame(editor_frame, bg=frame_color)
        editor_inner.pack(fill=tk.BOTH, expand=True)

        # execute button 
        self.execute_btn = tk.Button(editor_inner, text="EXECUTE",
                                     command=self.execute_code,
                                     bg=accent_blue, fg=button_fg,
                                     font=("Helvetica", 10, "bold"),
                                     cursor="hand2", padx=5, pady=5,
                                     activebackground="#005a9e", activeforeground="white")
        self.execute_btn.pack(anchor="ne", padx=10, pady=5)

        # text editor area below the button
        self.text_editor = scrolledtext.ScrolledText(editor_inner, wrap=tk.WORD,
                                                     font=("Consolas", 11),
                                                     bg=text_bg, fg=text_fg,
                                                     insertbackground="white",  # white cursor
                                                     selectbackground="#264f78")
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        # default code
        default_code = """HAI\nI HAS A var ITZ 12\nVISIBLE var\nI HAS A noot ITZ "var"\nKTHXBYE"""
        self.text_editor.insert("1.0", default_code)
        #------------------------------------------------------------------------------------------------------------
        # right panel (for lexemes and the symbol table)
        right_panel = tk.Frame(top_section, bg=bg_color, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # lexemes (list of tokens)
        lexemes_frame = tk.LabelFrame(right_panel, text="Lexemes", 
                                      font=("Helvetica", 10, "bold"), bg=frame_color, fg=text_fg)
        lexemes_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # treeviwew for lexemes
        lexeme_container = tk.Frame(lexemes_frame, bg=frame_color)
        lexeme_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        lexeme_scroll = tk.Scrollbar(lexeme_container)
        lexeme_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=frame_color, 
                        foreground=text_fg, fieldbackground=frame_color, rowheight=22)
        style.configure("Treeview.Heading", background=accent_blue, foreground="white", font=("Helvetica", 9, "bold"))
        style.map("Treeview", background=[("selected", "#094771")])
        
        self.lexeme_tree = ttk.Treeview(lexeme_container, columns=("Lexeme", "Classification"),
                                        show="headings", yscrollcommand=lexeme_scroll.set,
                                        height=10)
        self.lexeme_tree.heading("Lexeme", text="Lexeme")
        self.lexeme_tree.heading("Classification", text="Classification")
        self.lexeme_tree.column("Lexeme", width=120, anchor="w")
        self.lexeme_tree.column("Classification", width=250, anchor="w")
        self.lexeme_tree.pack(fill=tk.BOTH, expand=True)
        lexeme_scroll.config(command=self.lexeme_tree.yview)
        
        # symbol table section
        symbol_frame = tk.LabelFrame(right_panel, text="Symbol Table", 
                                     font=("Helvetica", 10, "bold"), bg=frame_color, fg=text_fg)
        symbol_frame.pack(fill=tk.BOTH, expand=True)
        
        symbol_container = tk.Frame(symbol_frame, bg=frame_color)
        symbol_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        symbol_scroll = tk.Scrollbar(symbol_container)
        symbol_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.symbol_tree = ttk.Treeview(symbol_container, columns=("Identifier", "Value"),
                                       show="headings", yscrollcommand=symbol_scroll.set,
                                       height=10)
        self.symbol_tree.heading("Identifier", text="Identifier")
        self.symbol_tree.heading("Value", text="Value")
        self.symbol_tree.column("Identifier", width=120, anchor="w")
        self.symbol_tree.column("Value", width=250, anchor="w")
        self.symbol_tree.pack(fill=tk.BOTH, expand=True)
        symbol_scroll.config(command=self.symbol_tree.yview)
        #------------------------------------------------------------------------------------------------------------
        # bottom container 
        console_pane = tk.Frame(paned_window, bg=bg_color)
        paned_window.add(console_pane, minsize=100)
        
        console_frame = tk.LabelFrame(console_pane, text="Console", 
                                      font=("Helvetica", 10, "bold"), bg=frame_color, fg=text_fg)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        self.console = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD,
                                                font=("Consolas", 10),
                                                bg=console_bg, fg=console_fg,
                                                insertbackground="white",
                                                height=8)
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
        self.console.insert("1.0", "Welcome to LOLCode Interpreter! Press 'Execute' to run your program.\n")
        self.console.insert("2.0", "=" * 50 + "\n")
        self.console.config(state=tk.DISABLED)
    #------------------------------------------------------------------------------------------------------------
    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Select LOLCode File",
            filetypes=[("LOL Files", "*.lol"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                    self.text_editor.delete("1.0", tk.END)
                    self.text_editor.insert("1.0", content)
                    self.current_file = filename
                    self.file_label.config(text=filename)
                    self.write_to_console(f"Loaded file: {filename}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
    #------------------------------------------------------------------------------------------------------------
    def execute_code(self):
        # reset previous executions
        self.clear_displays()
        
        # get code from thwe text editor section
        code = self.text_editor.get("1.0", tk.END).strip()
        
        if not code:
            self.write_to_console("Error: No code to execute!\n")
            return
        
        self.write_to_console("Executing code...\n")
        self.write_to_console("=" * 50 + "\n")
        
        # run lexer
        tokens, error = lexer.run("editor", code)
        
        if error:
            self.write_to_console(f"LEXICAL ERROR: {error.as_string()}\n")
            return
        
        # store tokens
        self.tokens = tokens
        
        # update lexeme table
        self.update_lexeme_table(tokens)
        
        # parse and execute 
        self.interpret_code(tokens)
        
        self.write_to_console("\n" + "=" * 50 + "\n")
        self.write_to_console("Execution completed!\n")
    #------------------------------------------------------------------------------------------------------------
    def update_lexeme_table(self, tokens):
        for token in tokens:
            lexeme = token.value if token.value is not None else token.type
            classification = token.type
            self.lexeme_tree.insert("", tk.END, values=(lexeme, classification))
    #------------------------------------------------------------------------------------------------------------
    def update_symbol_table(self, identifier, value):
        self.symbol_table[identifier] = value
        
        # clear and repopulate symbol table
        for item in self.symbol_tree.get_children():
            self.symbol_tree.delete(item)
        
        for var_name, var_value in self.symbol_table.items():
            self.symbol_tree.insert("", tk.END, values=(var_name, var_value))
    #------------------------------------------------------------------------------------------------------------
    def interpret_code(self, tokens):
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # handle variable declaration I HAS A var ITZ value
            if token.type == "Variable Declaration":  # I HAS A 'to
                if i + 2 < len(tokens):
                    var_name = tokens[i + 1].value  # variable name
                    # check for ITZ (assignment)
                    if i + 2 < len(tokens) and tokens[i + 2].type == "Variable Assignment":
                        if i + 3 < len(tokens):
                            value = tokens[i + 3].value
                            self.update_symbol_table(var_name, value)
                            i += 4
                            continue
                    else:
                        # varialble declared without value (NOOB)
                        self.update_symbol_table(var_name, None)
                        i += 2
                        continue
            
            # handle VISIBLE (output)
            elif token.type == "Output Keyword":  # VISIBLE
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if next_token.type == "varident":
                        # print variable value
                        var_name = next_token.value
                        if var_name in self.symbol_table:
                            self.write_to_console(f"{self.symbol_table[var_name]}\n")
                        else:
                            self.write_to_console(f"Error: Variable '{var_name}' not found\n")
                    else:
                        # print literal value
                        self.write_to_console(f"{next_token.value}\n")
                    i += 2
                    continue
            
            # handle assignment ==> var R value
            elif token.type == "varident" and i + 2 < len(tokens):
                if tokens[i + 1].type == "Assignment Operation":  # R
                    var_name = token.value
                    value = tokens[i + 2].value
                    self.update_symbol_table(var_name, value)
                    i += 3
                    continue
            
            i += 1
    #------------------------------------------------------------------------------------------------------------
    def write_to_console(self, text):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, text)
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
    #------------------------------------------------------------------------------------------------------------
    def clear_displays(self):
        for item in self.lexeme_tree.get_children():
            self.lexeme_tree.delete(item)
        
        for item in self.symbol_tree.get_children():
            self.symbol_tree.delete(item)
        
        self.symbol_table = {}
        
        self.console.config(state=tk.NORMAL)
        self.console.delete("1.0", tk.END)
        self.console.config(state=tk.DISABLED)


root = tk.Tk()
app = LOLCodeGUI(root)
root.mainloop()