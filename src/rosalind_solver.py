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
import standard_funcs


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    root = tb.Window(themename='solar')
    root.title('Rosalind Solver')
    root.geometry('1024x768')

    # Styles
    button_style = tb.Style()
    button_style.configure('.', font=('Calibri', 15, 'bold'))

    # Create notebook 
    notebook = tb.Notebook(root, bootstyle = "dark")
    notebook.pack(padx=10, pady=10)

    # Create tabs for each rosalind solution
    basics_tab = tb.Frame(notebook)
    notebook.add(basics_tab, text='Basics')
    basics_tab.grid_propagate = False

    fib_tab = tb.Frame(notebook)
    notebook.add(fib_tab, text='Fib')
    fib_tab.grid_propagate = False

    motif_tab = tb.Frame(notebook)
    notebook.add(motif_tab, text='Fastas')
    motif_tab.grid_propagate = False

    # Basics tab
    def basic_count():
        """ Count bases in entry on button press """

        out = ''

        if not standard_funcs.is_NA(basics_entry.get("1.0", "end-1c").rstrip('\n')):
            out = "(this doesn't seem to be a nucleic acid sequence)\n"

        counts = standard_funcs.count_bases(basics_entry.get("1.0", "end-1c").rstrip('\n'))

        if counts:
            max_width = len(str(max(counts.values())))+1

        for key in counts:
            out += f'{key: <{max_width}}'
        out += '\n'
        for key in counts:
            out += f'{counts[key]: <{max_width}}'

        basics_out.config(state='normal')
        basics_out.delete('1.0', 'end')
        basics_out.insert('1.0', f'{out}')
        basics_out.config(state=DISABLED)

    def basic_transcribe():
        """ Transcribe entry on button press """

        out = 'Not a valid nucleic acid sequence'
        if standard_funcs.is_NA(basics_entry.get('1.0', 'end-1c').rstrip('\n')):
            out = standard_funcs.transcribe(basics_entry.get("1.0", "end-1c").rstrip('\n'))

        basics_out.config(state='normal')
        basics_out.delete('1.0', 'end')
        basics_out.insert('1.0', f'{out}')
        basics_out.config(state=DISABLED)

    def basic_revc():
        """ Revc of entry on button press """

        out = 'Not a valid nucleic acid sequence'
        if standard_funcs.is_NA(basics_entry.get('1.0', 'end-1c').rstrip('\n')):
            out = standard_funcs.get_revc(basics_entry.get("1.0", "end-1c").rstrip('\n'))

        basics_out.config(state='normal')
        basics_out.delete('1.0', 'end')
        basics_out.insert('1.0', f'{out}')
        basics_out.config(state=DISABLED)

    def basic_gc():
        """ Compute GC of entry on button press """

        out = 'Not a valid nucleic acid sequence'
        if standard_funcs.is_NA(basics_entry.get('1.0', 'end-1c').rstrip('\n')):
            out = standard_funcs.get_gc(basics_entry.get("1.0", "end-1c").rstrip('\n'))

        basics_out.config(state='normal')
        basics_out.delete('1.0', 'end')
        basics_out.insert('1.0', f'{out}')
        basics_out.config(state=DISABLED)

    def basic_translate():
        """ Translate entry on button press """

        out = 'Not a valid nucleic acid sequence'
        if standard_funcs.is_NA(basics_entry.get('1.0', 'end-1c').rstrip('\n')):
            out = standard_funcs.translate(basics_entry.get("1.0", "end-1c").rstrip('\n'))

        basics_out.config(state='normal')
        basics_out.delete('1.0', 'end')
        basics_out.insert('1.0', f'{out}')
        basics_out.config(state=DISABLED)


    basics_exp = tb.Frame(basics_tab, borderwidth=10, height=200, width=1000, bootstyle="dark")
    basics_exp.pack(padx=10, pady=10, anchor='w')

    basics_text = tb.Text(basics_exp, font='Calibri, 15', height=15, width=200)
    basics_text.pack(fill='both', expand=True)
    basics_text.insert('1.0', 'Basic operations on nucleic acid sequences.\n\n\n'
                       'Count: Counts all bases (https://rosalind.info/problems/dna/)\n\n'
                       'Transcribe: Transcribes DNA into RNA (https://rosalind.info/problems/rna/)\n\n'
                       'Rev complement: Gives the reverse complement (https://rosalind.info/problems/revc/)\n\n'
                       'GC content: Calculates the GC content (https://rosalind.info/problems/gc/)\n\n'
                       'Translate: Translates a DNA or RNA sequence, irrespective of ORF, start, or stop\n(https://rosalind.info/problems/prot/)')
    basics_text.config(state=DISABLED)

    basics_inp = tb.Frame(basics_tab, borderwidth=10, height=500, width=1000, bootstyle="dark")
    basics_inp.pack(padx=10, pady=5, anchor='w')

    basics_entry = tb.ScrolledText(basics_inp, height=6, width=130)
    basics_entry.grid(row=0, column=0, columnspan=6, sticky='W')

    basecount_button = tb.Button(basics_inp, bootstyle="light", text="Count bases", command=basic_count)
    basecount_button.grid(row=1, column=0, pady=5, sticky='W')

    transcribe_button = tb.Button(basics_inp, bootstyle="light", text="Transcribe", command=basic_transcribe)
    transcribe_button.grid(row=1, column=1, pady=5, sticky='W')

    revc_button = tb.Button(basics_inp, bootstyle="light", text="Rev complement", command=basic_revc)
    revc_button.grid(row=1, column=2, pady=5, sticky='W')

    gc_button = tb.Button(basics_inp, bootstyle="light", text="GC content", command=basic_gc)
    gc_button.grid(row=1, column=3, pady=5, sticky='W')

    translate_button = tb.Button(basics_inp, bootstyle="light", text="Translate", command=basic_translate)
    translate_button.grid(row=1, column=4, sticky='W')

    basics_out = tb.ScrolledText(basics_inp, height=6, width=130)
    basics_out.config(state=DISABLED)
    basics_out.grid(row=2, column=0, columnspan=6, sticky='W')


    #fib tab
    def fib_calc():
        """ Calculates fibonacci from entries """

        litter = fib_litterentry.get()
        gen = fib_genentry.get()
        months = fib_deathentry.get()

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
            fib_results.config(text=f'Number of rabbits:{newline*2}'
                               f'  gen {"": <2} rabbits {newline}' 
                               f'{newline.join(f"  {i+1: <6} {standard_funcs.fib(i+1, int(litter)): <2}" for i in range(int(gen))[-10:])}')

        if months:
            fib_results.config(text=f'Number of rabbits:{newline*2}'
                               f'  gen {"": <2} rabbits {newline}' 
                               f'{newline.join(f"  {i+1: <6} {standard_funcs.fibd(i+1, int(months), int(litter))[0]: <2}" for i in range(int(gen))[-10:])}')

    fib_exp = tb.Frame(fib_tab, height=350, width=1000, bootstyle="dark")
    fib_exp.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    fib_exp.grid_propagate(False)

    fib_text = tb.Text(fib_exp, font='Calibri, 15', height=15, width=100)
    fib_text.pack(fill='both', expand='True')
    fib_text.insert('1.0', 'Calculates the number of rabbit pairs after n months, supposing each pair takes one month\nto mature, ' +
                       'can mate once a month and always produces a litter of the same size. \n\n' +
                       'https://rosalind.info/problems/fib/ \n\n\n\n' +
                       'Optionally, we can assume rabbits die after a defined number of months. \n\n' + 
                       'https://rosalind.info/problems/fibd/')
    fib_text.config(state=DISABLED)

    fib_inp = tb.Frame(fib_tab, borderwidth=10, height=350, width=970, bootstyle="dark")
    fib_inp.grid(row=1, column=0, padx=10, pady=10)
    fib_inp.grid_propagate(False)

    fib_inpinp = tb.Frame(fib_inp, bootstyle="dark", height=275, width=550)
    fib_inpinp.grid(row=0, column=0, padx=5, pady=40, sticky="w")
    fib_inpinp.grid_propagate = False

    fib_litterlabel = tb.Label(fib_inpinp, bootstyle='default', text='Litter size')
    fib_litterlabel.grid(row=0, column=0, sticky="W")

    fib_litterentry = tb.Entry(fib_inpinp, bootstyle='default', width=2)
    fib_litterentry.grid(row=0, column=1, padx=20, sticky="E")

    fib_genlabel = tb.Label(fib_inpinp, bootstyle='default', text='Generations')
    fib_genlabel.grid(row=1, column=0, sticky="W")

    fib_genentry = tb.Entry(fib_inpinp, bootstyle='default', width=2)
    fib_genentry.grid(row=1, column=1, pady=15, padx=20, sticky="E")

    fib_deathlabel = tb.Label(fib_inpinp, bootstyle='default', text='Months until death')
    fib_deathlabel.grid(row=2, column=0, sticky="W")

    fib_deathentry = tb.Entry(fib_inpinp, bootstyle='default', width=2)
    fib_deathentry.grid(row=2, column=1, padx=20, sticky="E")

    fib_calc_button = tb.Button(fib_inpinp, bootstyle="default", text='Calculate', command=fib_calc)
    fib_calc_button.grid(row=3, column=0, columnspan=3, pady=40)

    fib_inpout = tb.Frame(fib_inp, bootstyle='light', width=400, height=275)
    fib_inpout.grid(row=0, column=1, padx=50, pady=5, sticky="nw")
    fib_inpout.grid_propagate = False

    fib_results = tb.Label(fib_inpout, bootstyle='default', text='Number of rabbits: ')
    fib_results.grid(row=0, column=0, sticky='nswe')


    #motif tab
    def browse_dirs():
        """ Open directory browser """

        global path
        path = os.path.dirname(askopenfilename(title="Browse directory", 
                                               filetypes=(
                                                   ('FASTA files', ('*.fasta', '*.fa', '*.fna', '*.faa')),
                                                   ('FASTQ files', ('*.fastq', '*.fq')))))
        path_ent.delete(0, 'end')
        path_ent.insert(0, path)

        global fastx_files
        fastx_files = [os.path.join(path, file) for file in os.listdir(path) 
                       if os.path.isfile(os.path.join(path, file)) 
                       and standard_funcs.guess_format(f'{file}') in ['fasta', 'fastq']]

        motif_output.config(state='normal')
        motif_output.delete('1.0', 'end')
        motif_output.insert('1.0', standard_funcs.list_seqinfo(fastx_files))
        motif_output.config(state='disabled')

    motif_exp = tb.Frame(motif_tab, height=350, width=950, bootstyle="dark")
    motif_exp.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    motif_exp.grid_propagate(False)

    motif_text = tb.Text(motif_exp, font='Calibri, 15', height=15, width=94)
    motif_text.pack(fill='both', expand='True', anchor='center')
    motif_text.insert('1.0', 'Some operations for handling multiple sequences.\n' 
                      'Selecting any file will read out all fastX files in the directory. \n\n'
                      'Motif:\nFind the given motif in all sequences '
                      '(https://rosalind.info/problems/subs/)\n\n'
                      'Consensus: \nFind the consensus string of sequences of equal length '
                      '(https://rosalind.info/problems/cons/)\n\n'
                      'Graph: \nFind the overlap graphs of all sequences '
                      '(https://rosalind.info/problems/grph/)\n\n'
                      'Substring: \nFind the longest common substring in all sequences '
                      '(https://rosalind.info/problems/lcsm/)\n\n'
                      'Superstring: \nFind the shortest superstring containing all given sequences '
                      '(https://rosalind.info/problems/long/)')
    motif_text.config(state=DISABLED)

    #Input frame
    motif_inp = tb.Frame(motif_tab, borderwidth=10, height=50, width=950, bootstyle="dark")
    motif_inp.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
    motif_inp.grid_propagate(False)

    #Path input
    path = os.getcwd()
    path_row = tb.Frame(motif_inp)
    path_row.pack(fill='both', expand='True')
    path_lbl = tb.Label(path_row, text="Fasta dir:", width=10)
    path_lbl.pack(side='left', padx=10)
    path_ent = tb.Entry(path_row, width=80)
    path_ent.pack(side='left', fill='both', expand='True', padx=5)
    path_ent.insert(0, path)
    browse_btn = tb.Button(
        master=path_row, 
        text="Browse", 
        command=browse_dirs, 
        width=8
    )
    browse_btn.pack(side='right', padx=10)

    #Button frame
    motif_but = tb.Frame(motif_tab, height=270, width=270, bootstyle="dark")
    motif_but.grid(row=2, column=0, sticky='nw', padx=10, pady=10)
    motif_but.grid_propagate = False

    #Output frame
    motif_out = tb.Frame(motif_tab, height=270, width=900, bootstyle="dark")
    motif_out.grid(row=2, column=1, pady=10, sticky='nw')
    motif_out.grid_propagate = False

    motif_output = tb.Text(motif_out, height=15, width=60, font=('Calibri',13))
    motif_output.pack()
    motif_output.configure(state='disabled')

    root.mainloop()


# --------------------------------------------------
if __name__ == '__main__':
    main()
