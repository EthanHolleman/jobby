from pathlib import Path
import os
import subprocess
import logging
from datetime import datetime
from jobby import SBATCH_SIGNATURE

class Job():
    '''Job objects represent a batch job that is to be sumbitted to
    a workload manager, such as SLURM.
    '''
    SUBMIT = 'sbatch'

    def __init__(self, name, work_dir, template):
        self.name = name
        self.work_dir = work_dir
        self.template = template
        self.logger = self._make_logger()
        self.fields = []

    def execute(self):
        '''Submits the job to the workload manager. Before doing so
        writes an sbatch file based on the content of the fields
        attribute and saves a copy of that file in the _history_dir
        directory.
        '''
        self._write_sbatch()
        self._save_sbatch_copy()
        os.system(f'{Job.SUBMIT} {self._sbatch_path}')
        self.logger.info('Submitted sbatch job')

    @property
    def work_dir(self):
        return self._work_dir
    
    @work_dir.setter
    def work_dir(self, new_dir):
        new_dir_temp = Path(new_dir)
        if not new_dir_temp.is_dir():
            new_dir_temp.mkdir(parents=True)
        
        self._work_dir = new_dir_temp
    
    @property
    def _meta_dir(self):
        '''
        Returns:
            Path: Path to meta data directory for this job. Stores
        the log file.
        '''
        return self._dir_from_work_dir('meta')
    
    @property
    def _output_dir(self):
        '''
        Returns:
            Path: Path to output directory for the job.
        '''
        return self._dir_from_work_dir('output')
    
    @property
    def _sbatch_path(self):
        '''
        Returns:
            Path: Path to sbatch file that will be run when execute is called.
        '''
        return self.work_dir.joinpath(f'{self.name}.sbatch')
    
    @property
    def _log_path(self):
        '''
        Returns:
            Path: Path to log file.
        '''
        return self._meta_dir.joinpath(f'{self.name}.log')
    
    @property
    def _history_dir(self):
        '''
        Returns:
            Path: Path to history dir where dated copies of sbatch files are 
            saved.
        '''
        return self._dir_from_work_dir('history')
    
    @property
    def keyword_dict(self):
        '''
        Returns:
            dict: Dictionary that maps sbatch keywords with their replacement
            value
        '''
        return {
            "<name>": self.name,
            "<wd>": self.work_dir,
            "<od>": self._output_dir,
            "<time>": datetime.now(),
            "<sign>": SBATCH_SIGNATURE
        }

    def _dir_from_work_dir(self, name):
        '''Private helper method that creates a child directory in
        the `working_dir` directory. If child does not exist it is
        created.

        Args:
            name (str): Name of child directory.

        Returns:
            Path: Path to child directory.
        '''
        child = self.work_dir.joinpath(name)
        if not child.is_dir():
            child.mkdir()
        return child
    
    def _write_sbatch(self, path=None):
        '''Private helper method that writes an sbatch file.

        Args:
            path (Path, optional): Filepath to write to. Defaults to None. If
            None then is set to value of `_sbatch_path` property.
        '''
        if not path:
            path = self._sbatch_path
        with open(str(path), 'w') as sbatch_handle:
            text = self.template.fill(
                self.fields, keyword_dict=self.keyword_dict
                )
            sbatch_handle.write(text)
            self.logger.info(f'Wrote sbatch file {self._sbatch_path}')
    
    def _save_sbatch_copy(self):
        '''Private method that saves a copy of sbatch file to the histroy
        directory.
        '''
        copy = self._history_dir.joinpath(f'{self.name}_{datetime.now()}')
        self._write_sbatch(path=copy)
    
    def _make_logger(self):
        '''Private method that creates a logger object specific to the job.
        Logs are then saved in the meta directory of the job.

        Returns:
            Logger: Python logger object for this job.
        '''
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
        '%(levelname)s\t%(asctime)s\t%(name)s\t%(message)s')
        file_handler = logging.FileHandler(str(self._log_path))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    



    


    
    
    

    
    
    
    

    

    