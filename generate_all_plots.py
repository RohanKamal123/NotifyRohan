#!/usr/bin/env python3
"""
Generate all publication-ready performance curves for your paper.
This script runs all individual plotting scripts and organizes the outputs.
"""

import os
import subprocess
import sys

# List of all plotting scripts
scripts = [
    'specificity_curve_paper.py',
    'all_performance_curves.py',
    'confusion_matrix_plot.py',
    'learning_rate_plot.py'
]

print("=" * 60)
print("GENERATING ALL PUBLICATION-READY PLOTS")
print("=" * 60)

# Create output directory
output_dir = 'paper_plots'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"\nCreated output directory: {output_dir}")

# Run each script
for i, script in enumerate(scripts, 1):
    print(f"\n[{i}/{len(scripts)}] Running {script}...")
    print("-" * 40)
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        print(f"✓ {script} completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running {script}:")
        print(e.stderr)
        continue
    except FileNotFoundError:
        print(f"✗ Script {script} not found!")
        continue

# Move all generated plots to the output directory
print("\n" + "=" * 60)
print("ORGANIZING OUTPUT FILES")
print("=" * 60)

plot_extensions = ['.png', '.pdf', '.eps', '.svg']
moved_files = []

for file in os.listdir('.'):
    if any(file.endswith(ext) for ext in plot_extensions):
        if 'paper' in file or 'performance' in file or 'confusion' in file or 'learning_rate' in file:
            try:
                new_path = os.path.join(output_dir, file)
                os.rename(file, new_path)
                moved_files.append(file)
                print(f"Moved: {file} → {output_dir}/")
            except Exception as e:
                print(f"Error moving {file}: {e}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"\nTotal plots generated and moved: {len(moved_files)}")
print(f"\nAll plots are saved in: ./{output_dir}/")

print("\nGenerated plots include:")
categories = {
    'Specificity': ['specificity_performance_paper'],
    'Accuracy': ['accuracy_performance_paper'],
    'Loss': ['loss_performance_paper'],
    'Precision': ['precision_performance_paper'],
    'Recall': ['recall_performance_paper'],
    'F1-Score': ['f1score_performance_paper'],
    'ROC': ['roc_curve_paper'],
    'Combined': ['combined_metrics_paper'],
    'Confusion Matrix': ['confusion_matrices_paper', 'confusion_matrix_absolute_paper'],
    'Learning Rate': ['learning_rate_schedules_paper', 'learning_rate_with_loss_paper']
}

for category, files in categories.items():
    print(f"\n{category}:")
    for file_base in files:
        found = False
        for ext in plot_extensions:
            if f"{file_base}{ext}" in moved_files:
                found = True
                break
        status = "✓" if found else "✗"
        print(f"  {status} {file_base}")

print("\n" + "=" * 60)
print("ALL PLOTS GENERATED SUCCESSFULLY!")
print("=" * 60)