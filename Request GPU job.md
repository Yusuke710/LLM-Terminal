# Can you write me a script to use GPU?

## Sources
 1. https://docs.restech.unsw.edu.au/using_katana/running_jobs/
2. https://docs.restech.unsw.edu.au/help_support/glossary/
3. https://docs.restech.unsw.edu.au/using_katana/tips_katana/
4. https://docs.restech.unsw.edu.au/storage/data_archive/
5. https://docs.restech.unsw.edu.au/software/environment_modules/

 ## Answer

Here's a sample script for submitting a batch job on the Katana cluster that utilizes GPU resources. This script assumes that you want to run a program that requires one GPU and specifies the necessary memory and CPU resources.

```bash
#!/bin/bash
#PBS -l select=1:ncpus=6:ngpus=1:mem=46gb,walltime=12:00:00
#PBS -M your.name.here@unsw.edu.au
#PBS -m ae
#PBS -j oe
#PBS -o /home/z1234567/job_output.log

# Change to the working directory where the job is submitted from
cd $PBS_O_WORKDIR

# Load the necessary modules for your program
module load your_gpu_software_module  # Replace with the actual GPU software module you need

# Run your program
./your_program_executable  # Replace with the actual command to run your program
```

### Explanation of the Script:
- The `#!/bin/bash` line specifies that the script should be executed using the bash shell.
- The `#PBS -l` line specifies the resources required for the job:
  - `select=1` indicates that one node will be allocated.
  - `ncpus=6` requests six CPU cores.
  - `ngpus=1` requests one GPU.
  - `mem=46gb` allocates 46 GB of RAM.
  - `walltime=12:00:00` sets the maximum runtime for the job to 12 hours.
- The `#PBS -M` line specifies the email address to receive notifications regarding the job's status.
- The `#PBS -m ae` option sets notifications for job aborts and ends.
- The `#PBS -j oe` merges standard output and error into a single output file.
- The `#PBS -o` option sets the output file name for the job logs.
- The `cd $PBS_O_WORKDIR` command changes the working directory to the one from which the job was submitted.
- The `module load your_gpu_software_module` command loads the necessary GPU software module (replace it with the actual module name).
- Finally, the `./your_program_executable` line runs the desired executable program.

Make sure to replace placeholders with your actual job details and paths before submitting the script. Adjust the resource requests according to your specific needs and the requirements of your program.

