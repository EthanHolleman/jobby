import cmd2
import sys
import argparse
from jobby.template import Template
from jobby.job import Job
from jobby import *


class JobbyInterface(cmd2.Cmd):
    '''Defines the command line interface for the Jobby program.
    '''
    def __init__(self):
        super().__init__()
        self.prompt = '(Jobby) '
        self.debug = True
    
    def _print_error(self, message):
        '''Private helper method for printing error messages.

        Args:
            message (str): Message to print.
        '''
        self.poutput(
            f'{bcolors.FAIL}{message}{bcolors.ENDC}'
        )
    
    def _print_header_text(self, message):
        self.poutput(
            f'{bcolors.HEADER}{message}\n{"="*len(message)}{bcolors.ENDC}'
        )

    def _sbatch_args():
        '''Private method that uses argparser to provide command line
        args for do_sbatch.

        Returns:
            ArgParser: Parsed arguments
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--template', help='Path to sbatch template')
        parser.add_argument('-w', '--working_dir', help='Path to run job from')
        parser.add_argument('-n', '--name', help='Name of the job')
        parser.add_argument('-l', '--list_templates', action="store_true", 
                            help='List all templates stored by Jobby')
        return parser
    
    @cmd2.with_argparser(_sbatch_args())
    def do_sbatch(self, args):
        '''Submits an batch job to SLURM workload manager and creates a
        directory for that job. Jobs can be submitted using standard batch file
        syntax or include Jobby formating syntax. 
        

        Args:
            args ArgParser: Program command line arguments
        '''
        if args.list_templates:
            self._list_templates()
            return 0

        template = Template(args.template)
        job = Job(args.name, args.working_dir, template)
        filled_fields = []

        try:
            fillable_fields = template.fields
        except FileNotFoundError as e:
            self._print_error(f'Template file {args.template} not found!')
            return 1

        if fillable_fields:
            self.poutput(
            f'{bcolors.HEADER}Enter values for template fields{bcolors.ENDC}'
            )
            for field in fillable_fields:
                arg, default = field[1], field[2]
                message = f'{arg}, default = {default}: '
                entered_value = input(message)
                if not entered_value:
                    entered_value = default
                filled_fields.append(
                    (arg, entered_value)
                )
            job.fields = filled_fields

        job.execute()
    
    def _list_templates(self):
        self._print_header_text('Available Templates')
        for f in TEMPLATES_PATH.iterdir():
            self.poutput(
                f'{f.name}\t{f}'
            )

        
