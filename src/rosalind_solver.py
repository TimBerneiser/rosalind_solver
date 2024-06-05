"""
Author : Tim Berneiser
Date   : 2024-05-27
Purpose: GUI integrating my Rosalind solutions
"""

import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter.filedialog import askdirectory, askopenfilename
from PIL import ImageTk, Image
import standard_funcs


# --------------------------------------------------
class RosalindSolver(tb.Window):
    def __init__(self):

        # main setup
        super().__init__(themename='solar')
        self.title('')
        self.title('Rosalind Solver')
        self.geometry('1024x768')
        button_style = tb.Style()
        button_style.configure('.', font=('Calibri', 15, 'bold'))

        # notebook setup
        Notebook(self)


class Notebook(tb.Notebook):
    def __init__(self, parent):
        super().__init__(parent, bootstyle='dark')

        # Basics tab
        basics_tab = self.Page(self, 'Basics')
        Explanation(basics_tab, 'Basic operations on nucleic acid sequences.\n\n\n'
                                'Count: Counts all bases (https://rosalind.info/problems/dna/)\n\n'
                                'Transcribe: Transcribes DNA into RNA (https://rosalind.info/problems/rna/)\n\n'
                                'Rev complement: Gives the reverse complement (https://rosalind.info/problems/revc/)\n\n'
                                'GC content: Calculates the GC content (https://rosalind.info/problems/gc/)\n\n'
                                'Translate: Translates a DNA or RNA sequence, irrespective of ORF, start, or stop\n(https://rosalind.info/problems/prot/)', 
                                0.5)
        basics_output = tb.Frame(basics_tab)
        basics_output.place(x=0, rely=0.51, relwidth=1, relheight=0.49)
        BasicsTab(basics_output)

        # Fib tab
        fib_tab = self.Page(self, 'Fib')
        Explanation(fib_tab,    'Calculates the number of rabbit pairs after n months, supposing each pair takes one month\nto mature, ' +
                                'can mate once a month and always produces a litter of the same size. \n\n' +
                                'https://rosalind.info/problems/fib/ \n\n\n\n' +
                                'Optionally, we can assume rabbits die after a defined number of months. \n\n' + 
                                'https://rosalind.info/problems/fibd/', 
                                0.4)
        fib_output = tb.Frame(fib_tab)
        fib_output.place(x=0, rely=0.41, relwidth=1, relheight=0.59)
        FibTab(fib_output)

        # Fasta tab
        fastas_tab = self.Page(self, 'Fastas')
        Explanation(fastas_tab, 'Some operations for handling multiple sequences.\n' 
                                'Selecting any file will read out all fastX files in the directory. \n\n'
                                'Motif:\nFind the given motif in all sequences '
                                '(https://rosalind.info/problems/subs/)\n\n'
                                'Consensus: \nFind the consensus string of sequences of equal length '
                                '(https://rosalind.info/problems/cons/)\n\n'
                                'Substring: \nFind the longest common substring in all sequences '
                                '(https://rosalind.info/problems/lcsm/)\n\n'
                                'Superstring: \nFind the shortest superstring containing all given sequences '
                                '(https://rosalind.info/problems/long/)',
                                0.5)
        fastas_output = tb.Frame(fastas_tab)
        fastas_output.place(x=0, rely=0.51, relwidth=1, relheight=0.49)
        FastasTab(fastas_output)

        # Graph tab
        graph_tab = self.Page(self, 'Graph')
        Explanation(graph_tab,  'Create an overlap graph from the given sequences in FASTX format. Images are saved to a file\n'
                                'and opened by default. Check the box to print to the app instead (does not work well for large graphs).\n\n' 
                                'https://rosalind.info/problems/grph/',
                    0.2)
        graph_output = tb.Frame(graph_tab)
        graph_output.place(x=0, rely=0.21, relwidth=1, relheight=0.79)
        GraphTab(graph_output)

        self.pack(padx=10, pady=10, anchor='nw', fill='both', expand=True)

    class Page(tb.Frame):
        def __init__(self, parent, tab_name):
            super().__init__(parent)
            parent.add(self, text=tab_name)

class Explanation(tb.Frame):
    """ Insert explanation frame """

    def __init__(self, parent, expl_text, rel_height):
        super().__init__(parent, borderwidth=10, bootstyle='dark')

        self.place(x = 0, y = 0, relwidth=1, relheight= rel_height)

        self.expl_text = tb.Text(self, font='Calibri, 15')
        self.expl_text.pack(fill='both', expand=True)
        self.expl_text.insert('1.0', expl_text)
        self.expl_text.config(state=DISABLED)

class BasicsTab(tb.Frame):
    """ Input output for basics tab """

    def __init__(self, parent):
        super().__init__(parent, borderwidth=10, bootstyle='dark')
        self.pack(fill='both', expand=True)

        # Input field
        self.entry = tb.ScrolledText(self, height=6, width=130)
        self.entry.pack(fill='both', expand=True)
        self.entry.insert(1.0, 'Enter DNA sequence')

        # Row of buttons
        self.buttons_frame = tb.Frame(self)
        self.buttons_frame.pack(anchor='w')

        basecount_button = tb.Button(self.buttons_frame, bootstyle="light", text="Count bases", command=self.basic_count)
        basecount_button.grid(row=1, column=0, pady=5, padx=5)

        transcribe_button = tb.Button(self.buttons_frame, bootstyle="light", text="Transcribe", command=self.basic_transcribe)
        transcribe_button.grid(row=1, column=1, pady=15, padx=5, sticky='W')

        revc_button = tb.Button(self.buttons_frame, bootstyle="light", text="Rev complement", command=self.basic_revc)
        revc_button.grid(row=1, column=2, pady=15, padx=5, sticky='W')

        gc_button = tb.Button(self.buttons_frame, bootstyle="light", text="GC content", command=self.basic_gc)
        gc_button.grid(row=1, column=3, pady=15, padx=5, sticky='W')

        translate_button = tb.Button(self.buttons_frame, bootstyle="light", text="Translate", command=self.basic_translate)
        translate_button.grid(row=1, column=4, pady=15, padx=5, sticky='W')

        # Output field
        self.output = tb.ScrolledText(self, height=6, width=130)
        self.output.pack(fill='both', expand=True)
        self.output.config(state=DISABLED)

    # Button commands
    def basic_count(self):
        """ Count bases in entry on button press """

        out = ''

        if not standard_funcs.is_NA(self.entry.get('1.0', 'end-1c').rstrip('\n')):
            out = "(this doesn't seem to be a nucleic acid sequence)\n"

        counts = standard_funcs.count_bases(self.entry.get('1.0', 'end-1c').rstrip('\n'))

        if counts:
            max_width = len(str(max(counts.values())))+1

        for key in counts:
            out += f'{key: <{max_width}}'
        out += '\n'
        for key in counts:
            out += f'{counts[key]: <{max_width}}'

        self.output.config(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('1.0', f'{out}')
        self.output.config(state=DISABLED)

    def basic_transcribe(self):
        """ Transcribe entry on button press """

        out = 'Not a valid nucleic acid sequence'
        if standard_funcs.is_NA(self.entry.get('1.0', 'end-1c').rstrip('\n')):
            out = standard_funcs.transcribe(self.entry.get("1.0", "end-1c").rstrip('\n'))

        self.output.config(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('1.0', f'{out}')
        self.output.config(state=DISABLED)

    def basic_revc(self):
        """ Revc of entry on button press """

        out = 'Not a valid nucleic acid sequence'
        if standard_funcs.is_NA(self.entry.get('1.0', 'end-1c').rstrip('\n')):
            out = standard_funcs.get_revc(self.entry.get("1.0", "end-1c").rstrip('\n'))

        self.output.config(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('1.0', f'{out}')
        self.output.config(state=DISABLED)

    def basic_gc(self):
        """ Compute GC of entry on button press """

        out = 'Not a valid nucleic acid sequence'
        if standard_funcs.is_NA(self.entry.get('1.0', 'end-1c').rstrip('\n')):
            out = standard_funcs.get_gc(self.entry.get("1.0", "end-1c").rstrip('\n'))

        self.output.config(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('1.0', f'{out}')
        self.output.config(state=DISABLED)

    def basic_translate(self):
        """ Translate entry on button press """

        out = 'Not a valid nucleic acid sequence'
        if standard_funcs.is_NA(self.entry.get('1.0', 'end-1c').rstrip('\n')):
            out = standard_funcs.translate(self.entry.get("1.0", "end-1c").rstrip('\n'))

        self.output.config(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('1.0', f'{out}')
        self.output.config(state=DISABLED)

class FibTab(tb.Frame):
    """ Input output for Fib tab """

    def __init__(self, parent):
        super().__init__(parent, borderwidth=10, bootstyle='dark')
        self.pack(fill='both', expand=True)

        # Input frame
        self.input_frame = tb.Frame(self, bootstyle='dark', borderwidth=10)
        self.input_frame.place(x=0, rely=0.1, relheight=1, relwidth=0.4)

        self.litterlabel = tb.Label(self.input_frame, bootstyle='default', text='Litter size')
        self.litterlabel.grid(row=0, column=0, sticky="W")

        self.litterentry = tb.Entry(self.input_frame, bootstyle='default', width=2)
        self.litterentry.grid(row=0, column=1, padx=20, sticky="E")

        self.genlabel = tb.Label(self.input_frame, bootstyle='default', text='Generations')
        self.genlabel.grid(row=1, column=0, sticky="W")

        self.genentry = tb.Entry(self.input_frame, bootstyle='default', width=2)
        self.genentry.grid(row=1, column=1, pady=15, padx=20, sticky="E")

        self.deathlabel = tb.Label(self.input_frame, bootstyle='default', text='Months until death')
        self.deathlabel.grid(row=2, column=0, sticky="W")

        self.deathentry = tb.Entry(self.input_frame, bootstyle='default', width=2)
        self.deathentry.grid(row=2, column=1, padx=20, sticky="E")

        self.calc_button = tb.Button(self.input_frame, bootstyle="default", text='Calculate', command=self.calc_fib)
        self.calc_button.grid(row=3, column=0, columnspan=3, pady=40)

        # Output frame
        self.output_frame = tb.Frame(self, bootstyle='dark')
        self.output_frame.place(y=0, relx=0.4, relheight=1, relwidth=0.6)
        
        self.results = tb.Label(self.output_frame, bootstyle='default', text='Number of rabbits', anchor='nw', padding=15)
        self.results.pack(anchor='nw', expand=True, fill='both')
            #Output box

    def calc_fib(self):
        """ Calculates fibonacci from entries """

        litter = self.litterentry.get()
        gen = self.genentry.get()
        months = self.deathentry.get()

        if not litter.isdigit() or not gen.isdigit():
            Messagebox.ok(f'Please enter only natural numbers.', 'Invalid input')
            return

        if months and not months.isdigit():
            Messagebox.ok('Please enter only natural numbers.', 'Invalid input')
            return

        if not 0 < int(litter) < 11:
            Messagebox.ok('Litter size needs to be between 1 and 10.', 'Invalid input')
            return

        newline ="\n"

        if not months:
            self.results.config(text=f'Number of rabbits:{newline*2}'
                               f'  gen {"": <2} rabbits {newline*2}' 
                               f'{newline.join(f"  {i+1: <6} {standard_funcs.fib(i+1, int(litter)): <2}" for i in range(int(gen))[-10:])}')

        if months:
            self.results.config(text=f'Number of rabbits:{newline*2}'
                               f'  gen {"": <2} rabbits {newline*2}' 
                               f'{newline.join(f"  {i+1: <6} {standard_funcs.fibd(i+1, int(months), int(litter))[0]: <2}" for i in range(int(gen))[-10:])}')

class FastasTab(tb.Frame):
    """Input output for fastas tab"""

    def __init__(self, parent):
        super().__init__(parent, borderwidth=10, bootstyle='dark')
        self.pack(fill='both', expand=True)

        # Path input row
        path_frame = tb.Frame(self, borderwidth=10, bootstyle='dark')
        path_frame.pack(anchor='n')
        dir_label = tb.Label(path_frame, text="Fasta dir:", width=10)
        dir_label.pack(side='left', padx=10)
        self.dir_entry = tb.Entry(path_frame, width=80)
        self.dir_entry.pack(side='left', padx=5)
        self.dir_entry.insert(0, os.getcwd())
        browse_btn = tb.Button(
        master=path_frame, 
        text="Browse", 
        command=self.browse_dirs, 
        width=8)
        browse_btn.pack(side='right', padx=10)

        # Output frame
        output_frame = tb.Frame(self, borderwidth=10, bootstyle='dark')
        output_frame.pack(fill='both', expand=True)

        # Buttons
        buttons_frame = tb.Frame(output_frame, borderwidth=10, bootstyle='dark')
        buttons_frame.place(x=0, y=0, relheight=1, relwidth=0.3)

        motif_button = tb.Button(buttons_frame, bootstyle='light', width=15, text='Find motif', command=self.motif_click)
        motif_button.pack(pady=2,padx=10, anchor='nw')

        self.motif_input = tb.Entry(buttons_frame, width=19, font=('Calibri', 15))
        self.motif_input.pack(pady=2, padx=10, anchor='nw')

        consensus_button = tb.Button(buttons_frame, bootstyle='light', width=15, text='Consensus', command=self.consensus_click)
        consensus_button.pack(pady=8, padx=10, anchor='nw')

        substring_button = tb.Button(buttons_frame, bootstyle='light', width=15, text='Substring', command=self.substring_click)
        substring_button.pack(pady=8, padx=10, anchor='nw')

        superstring_button = tb.Button(buttons_frame, bootstyle='light', width=15, text='Superstring', command=self.superstring_click)
        superstring_button.pack(pady=8, padx=10, anchor='nw')

        # Output
        self.output = tb.Text(output_frame, font=('Calibri', 13), wrap=CHAR)
        self.output.place(y=0, relx=0.3, relheight=1, relwidth=0.7)
        self.output.configure(state='disabled')

    def motif_click(self):
        """ Find motif """

        motif_positions = {}

        for id in input_sequences:
            motif_positions[id] = standard_funcs.find_motifs(input_sequences[id], self.motif_input.get())

        self.output.config(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('1.0', f'{seq_info}\n\n\n')
        self.output.insert('end', f'Start indexes of motif "{self.motif_input.get()}":\n\n')
        for id in motif_positions:
            self.output.insert('end', f'{id}: {", ".join(str(x) for x in motif_positions[id])}\n')
        self.output.config(state='disabled')

    def consensus_click(self):
        """ Find consensus sequence """

        seqs_list = [input_sequences[id] for id in input_sequences]
    
        consensus = standard_funcs.find_consensus(seqs_list)

        self.output.config(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('1.0', f'{seq_info}\n\n\n')
        self.output.insert('end', f'Consensus sequence:\n\n')
        self.output.insert('end', consensus)
        self.output.config(state='disabled')

    def substring_click(self):
        """ Find longest substring """
        return

    def superstring_click(self):
        """ Find superstring """
        return

    def browse_dirs(self):
        """ Browse directory and get all fastas """

        path = os.path.dirname(askopenfilename(title="Browse directory", 
                                               filetypes=(
                                                   ('FASTA files', ('*.fasta', '*.fa', '*.fna', '*.faa')),
                                                   ('FASTQ files', ('*.fastq', '*.fq')))))
        self.dir_entry.delete(0, 'end')
        self.dir_entry.insert(0, path)

        global fastx_files
        fastx_files = [os.path.join(path, file) for file in os.listdir(path) 
                       if os.path.isfile(os.path.join(path, file)) 
                       and standard_funcs.guess_format(f'{file}') in ['fasta', 'fastq']]

        global seq_info
        seq_info = standard_funcs.list_seqinfo(fastx_files)

        self.output.config(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('1.0', seq_info)
        self.output.config(state='disabled')

        global input_sequences
        input_sequences = standard_funcs.extract_seqs(fastx_files)

class GraphTab(tb.Frame):
    """ Input output Graph tab """

    def __init__(self, parent):
        super().__init__(parent, borderwidth=10, bootstyle='dark')
        self.pack(fill='both', expand=True)

        # Input frame
        input_frame = tb.Frame(self, borderwidth=10, bootstyle='dark')
        input_frame.place(relx=0, rely=0, relheight=1, relwidth=0.3)

        file_label = tb.Label(input_frame, text='Fastx file: ', width=22)
        file_label.pack(anchor='w', padx=5, pady=10)

        self.file_ent = tb.Entry(input_frame, width=36)
        self.file_ent.pack(anchor='w', padx=5)
        self.file_ent.insert('end', os.getcwd())

        browse_button = tb.Button(input_frame, text="Browse", command=self.browse_file, width=10)
        browse_button.pack(anchor='w', padx=5, pady=10)

        overlap_frame = tb.Frame(input_frame)
        overlap_frame.pack(anchor='w', pady=20)

        overlap_label = tb.Label(overlap_frame, text='Overlap:', width=14)
        overlap_label.pack(side='left', padx=5)

        self.overlap_entry = tb.Entry(overlap_frame, width=1)
        self.overlap_entry.pack(side='left', padx=5, pady=5, anchor='w')

        save_frame = tb.Frame(input_frame)
        save_frame.pack(anchor='w')

        save_label = tb.Label(save_frame, text='Save output?', width=14)
        save_label.pack(side='left', padx=5, pady=5)

        self.open_image_var = tb.BooleanVar(value = True)
        save_checkbox = tb.Checkbutton(save_frame, variable=self.open_image_var)
        save_checkbox.pack(side='left', padx=5)

        # Output frame
        output_frame = tb.Frame(self, borderwidth=10, bootstyle='dark')
        output_frame.place(rely=0.1, relx=0.35, relheight=1, relwidth=0.65)

        self.output_image = tb.Label(output_frame, image='')


    def browse_file(self):
        """ Browse files and graph """
        file_path = askopenfilename(title="Browse directory", 
                               filetypes=(('FASTA files', ('*.fasta', '*.fa', '*.fna', '*.faa')),
                                          ('FASTQ files', ('*.fastq', '*.fq'))))
        self.file_ent.delete(0, 'end')
        self.file_ent.insert(0, file_path)

        if standard_funcs.guess_format(f'{file_path}') not in ['fasta', 'fastq'] and not file_path.rstrip() == '':
            Messagebox.ok('Not a valid fastx file.', 'Invalid input')
            return

        input_sequences = standard_funcs.extract_seqs([file_path])

        overlap = self.overlap_entry.get()
        overlap = overlap.rstrip()

        if not overlap.isdigit():
            Messagebox.ok('Not a valid overlap. Enter a positive integer.', 'Invalid input')
            return
        else:
            overlap = int(overlap)

        dot = standard_funcs.visualize_graphs(standard_funcs.list_overlaps(input_sequences, overlap))
        overlap_graph = f'{os.path.join(os.path.dirname(file_path), "out")}'
        dot.render(overlap_graph, view=self.open_image_var.get(), format='png')

        graph_image = Image.open(f'{overlap_graph}.png')

        if not self.open_image_var.get():
            base_width = 680
            wpercent = (base_width / float(graph_image.size[0]))
            hsize = int((float(graph_image.size[1]) * float(wpercent)))
            graph_image = graph_image.resize((base_width, hsize), Image.Resampling.LANCZOS)

            graph_image = ImageTk.PhotoImage(graph_image)
            self.output_image.config(image=graph_image)
            self.output_image.image = graph_image
            self.output_image.pack(side='top', fill='both', expand='true')

        if not self.open_image_var.get():
            os.remove(f'{overlap_graph}.png')
            os.remove(f'{overlap_graph}')


# --------------------------------------------------
if __name__ == '__main__':
    solver = RosalindSolver()
    solver.mainloop()