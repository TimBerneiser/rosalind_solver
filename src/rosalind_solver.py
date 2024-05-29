"""
Author : Tim Berneiser
Date   : 2024-05-27
Purpose: GUI integrating my Rosalind solutions
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
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

    fib_tab = tb.Frame(notebook)
    notebook.add(fib_tab, text='Fib')

    inh_tab = tb.Frame(notebook)
    notebook.add(inh_tab, text='Inh')

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

    fib_exp = tb.Frame(fib_tab, height=350, width=970, bootstyle="dark")
    fib_exp.grid(row=0, column=0, padx=10, pady=10)
    fib_exp.grid_propagate(False)

    fib_text = tb.Text(fib_exp, font='Calibri, 15', height=15, width=96)
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


    root.mainloop()


# --------------------------------------------------
if __name__ == '__main__':
    main()
