from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory

from GenerateFs import generate_fs
from Models import get_dadi_model_params

def main():
    root = Tk()
    root.title("Diffusion Approximation for Demographic Inference")
    root.geometry("500x250")
    root.rowconfigure(0, minsize=800, weight=1)
    root.columnconfigure(1, minsize=800, weight=1)
    root.resizable(width=True, height=True)
    root.option_add('*tearOff', False)

    # create a menubar
    menubar = Menu(root)
    
    # create commands for different analysis
    def create_new_window(title):
        window = Toplevel(root)
        window.title(title)
        
        return window
    
    def generate_fs_window():
        window = create_new_window("Generate frequency spectrum")
        
        frm = Frame(window)
        frm_sample_size = Frame(frm)
        params_labels = []
        params_entries = []
        pop_ids = []
        sample_size_entries = []
        
        def select_vcf_file():
            file_name = askopenfilename(
                parent=window,
                filetypes=[("GZcompressed VCF Files", "*.vcf.gz"), ("VCF Files", "*.vcf"), ("All Files", "*.*")]
            )
            if not file_name: return
            
            lbl_vcf['text'] = file_name
            
            return file_name
        
        def select_pop_info():
            
            for lbl in params_labels: lbl.destroy()
            for ent in params_entries: ent.destroy()
            
            file_name = askopenfilename(
                parent=window,
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not file_name: return
            
            lbl_pop_info['text'] = file_name
            
            pops = {}
            f = open(file_name, 'r')
            for line in f:
                elm = line.rstrip().split()
                pops[elm[1]] = 1
            f.close()
            i = 0
            for p in pops:
                pop_ids.append(p)
                lbl = Label(frm_sample_size, text=p)
                ent = Entry(frm_sample_size, width=10)
                
                params_labels.append(lbl)
                params_entries.append(ent)

                lbl.grid(row=0, column=i, sticky="ew", padx=5, pady=5)
                i += 1
                ent.grid(row=0, column=i, sticky="ew", padx=5, pady=5)
                i += 1
                sample_size_entries.append(ent)
            
            return file_name
        
        def output_file():
            file_name = asksaveasfilename(
                parent=window,
                defaultextension="fs",
                filetypes=[("Frequency Spectrum Files", "*.fs"), ("All Files", "*.*")],
            )
            if not file_name: return
            
            lbl_output['text'] = file_name
            return file_name
        
        def run_generate_fs():
            if is_unfolded.get() == 1: is_polarized = True
            else: is_polarized = False
            sample_sizes = []
            for e in sample_size_entries:
                sample_sizes.append(int(e.get()))
                
            generate_fs(
                vcf=lbl_vcf['text'], 
                output=lbl_output['text'], 
                pop_ids=pop_ids, 
                pop_info=lbl_pop_info['text'], 
                projections=sample_sizes, 
                polarized=is_polarized, 
                bootstrap=None, chunk_size=0)
        
        btn_select_vcf = Button(frm, text="Select a VCF file", command=select_vcf_file)
        btn_select_pop_info = Button(frm, text="Select a Pop Info file", command=select_pop_info)
        btn_select_output = Button(frm, text="Save as", command=output_file)
        btn_generate = Button(frm, width=10, text="Generate", command=run_generate_fs)
        
        lbl_vcf = Label(frm, text="No VCF file selected")
        lbl_pop_info = Label(frm, text="No Pop Info file selected")
        lbl_output = Label(frm, text="No output file")
        lbl_projections = Label(frm, text="Sample sizes (chromosomes)")
        
        is_unfolded = IntVar()
        cbt_unfolded = Checkbutton(frm, text="Unfolded", variable=is_unfolded)
        
        btn_select_vcf.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_select_pop_info.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        btn_select_output.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_generate.grid(row=5, column=2, sticky="ew", padx=5, pady=5)
        
        lbl_vcf.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        lbl_pop_info.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        lbl_output.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        lbl_projections.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        
        cbt_unfolded.grid(row=3, column=0, sticky="n", padx=5, pady=5)
        
        frm_sample_size.grid(row=4, column=1, sticky="ns")
        frm.grid(row=0, column=0, sticky="ns")
    
    def infer_dm_window():
        window = create_new_window("Infer demographic models")
        
        frm = Frame(window)
        frm_initial_values = Frame(frm)
        frm_upper_bounds = Frame(frm)
        frm_lower_bounds = Frame(frm)
        frm_fixed_params = Frame(frm)
        params_labels = []
        params_entries = []
        params_checkboxes = []
        
        def select_fs_file():
            file_name = askopenfilename(
                parent=window,
                filetypes=[("Frequency Spectrum Files", "*.fs"), ("All Files", "*.*")]
            )
            if not file_name: return
            
            lbl_fs['text'] = file_name
            
            return file_name
        
        def select_output_dir():
            file_dir = askdirectory(parent=window)
            
            if not file_dir: return
            
            lbl_output_dir['text'] = file_dir
            
            return file_dir
        
        def run_infer_dm():
            return
        
        btn_select_fs = Button(frm, text="Select a frequency spectrum file", command=select_fs_file)
        lbl_fs = Label(frm, text="No frequency spectrum file selected")   
        btn_select_fs.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        lbl_fs.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        btn_select_output_dir = Button(frm, text="Select a output directory", command=select_output_dir)
        lbl_output_dir = Label(frm, text="No output directory selected")
        btn_select_output_dir.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        lbl_output_dir.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        lbl_output_file_prefix = Label(frm, text="Output file prefix")
        ent_output_file = Entry(frm, width=50)
        lbl_output_file_prefix.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        ent_output_file.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        lbl_model = Label(frm, text="Select a demographic model")
        model_value = StringVar()
        cbb_models = ttk.Combobox(frm, textvariable=model_value)
        cbb_models['values'] = (
            'bottlegrowth_1d',
            'growth_1d',
            'snm_1d',
            'three_epoch_1d',
            'two_epoch_1d',
            'bottlegrowth_2d',
            'bottlegrowth_split',
            'bottlegrowth_split_mig',
            'IM',
            'IM_pre',
            'split_mig',
            'split_asym_mig',
            'snm_2d'
        )
        cbb_models.state(["readonly"])
        
        def select_models(event):
            
            for lbl in params_labels: lbl.destroy()
            for ent in params_entries: ent.destroy()
            for cbt in params_checkboxes: cbt.destroy()
            
            params = get_dadi_model_params(cbb_models.get())
            i = 0
            for p in params:
                lbl1 = Label(frm_initial_values, text=p)
                lbl2 = Label(frm_upper_bounds, text=p)
                lbl3 = Label(frm_lower_bounds, text=p)
                params_labels.append(lbl1)
                params_labels.append(lbl2)
                params_labels.append(lbl3)
                
                ent1 = Entry(frm_initial_values, width=10)
                ent2 = Entry(frm_upper_bounds, width=10)
                ent3 = Entry(frm_lower_bounds, width=10)
                params_entries.append(ent1)
                params_entries.append(ent2)
                params_entries.append(ent3)
                
                cbt = Checkbutton(frm_fixed_params, text=p)
                params_checkboxes.append(cbt)
                
                lbl1.grid(row=0, column=i, sticky="ew", padx=5, pady=5)
                lbl2.grid(row=0, column=i, sticky="ew", padx=5, pady=5)
                lbl3.grid(row=0, column=i, sticky="ew", padx=5, pady=5)
                cbt.grid(row=0, column=i, sticky="n", padx=5, pady=5)
                i += 1
                ent1.grid(row=0, column=i, sticky="ew", padx=5, pady=5)
                ent2.grid(row=0, column=i, sticky="ew", padx=5, pady=5)
                ent3.grid(row=0, column=i, sticky="ew", padx=5, pady=5)
                i += 1
            
        cbb_models.bind('<<ComboboxSelected>>', select_models)
        
        lbl_model.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        cbb_models.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        cbt_misid = Checkbutton(frm, text="Add misidentification")
        cbt_misid.grid(row=4, column=0, sticky="n", padx=5, pady=5)
        
        lbl_initial_values = Label(frm, text="Initial values")
        lbl_upper_bounds = Label(frm, text="Upper bounds")
        lbl_lower_bounds = Label(frm, text="Lower bounds")
        lbl_fixed_params = Label(frm, text="Fixed parameters")
        lbl_parallel_jobs = Label(frm, text="Parallel jobs")
        lbl_initial_values.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        lbl_upper_bounds.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        lbl_lower_bounds.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
        lbl_fixed_params.grid(row=8, column=0, sticky="ew", padx=5, pady=5)
        lbl_parallel_jobs.grid(row=9, column=0, sticky="ew", padx=5, pady=5)
        
        ent_parallel_jobs = Entry(frm, width=20)
        ent_parallel_jobs.grid(row=9, column=1, sticky="ew", padx=5, pady=5)
        
        btn_infer = Button(frm, width=10, text="Infer", command=run_infer_dm)
        btn_infer.grid(row=10, column=2, sticky="ew", padx=5, pady=5)
        
        frm_initial_values.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        frm_upper_bounds.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        frm_lower_bounds.grid(row=7, column=1, sticky="ew", padx=5, pady=5)
        frm_fixed_params.grid(row=8, column=1, sticky="ew", padx=5, pady=5)
        frm.grid(row=0, column=0, sticky="ns")

    def generate_cache_window():
        window = create_new_window("Generate cache for DFE inference")

    def infer_dfe_window():
        window = create_new_window("Infer DFEs")

    def analyze_uncerts_window():
        window = create_new_window("Analyze uncertainty")

    def make_plots_window():
        window = create_new_window("Make plots")

    # create a menu for analysis
    menu_analysis = Menu(menubar)
    menu_analysis.add_command(label="Generate frequency spectrum", command=generate_fs_window)
    menu_analysis.add_command(label="Infer demographic models", command=infer_dm_window)
    menu_analysis.add_command(label="Generate cache for DFE inference", command=generate_cache_window)
    menu_analysis.add_command(label="Infer DFEs", command=infer_dfe_window)
    menu_analysis.add_command(label="Analyze uncertainty", command=analyze_uncerts_window)
    menu_analysis.add_command(label="Make plots", command=make_plots_window)
    menubar.add_cascade(menu=menu_analysis, label='Analysis')

    # create a menu for help
    menu_help = Menu(menubar)
    
    menu_help.add_command(label="Manual")
    menu_help.add_command(label="Google group")
    menu_help.add_command(label="About")
    menubar.add_cascade(menu=menu_help, label='Help')

    root['menu'] = menubar

    root.mainloop()
    
if __name__ == '__main__':
    main()