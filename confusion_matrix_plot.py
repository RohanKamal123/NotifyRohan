import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Set style for publication
plt.style.use('seaborn-v0_8-whitegrid')

# Generate synthetic predictions for confusion matrix
np.random.seed(48)
n_samples = 1000
n_classes = 4  # For multi-class classification

# Generate true labels
y_true = np.random.randint(0, n_classes, n_samples)

# Generate predictions with some realistic error patterns
y_pred_train = y_true.copy()
y_pred_val = y_true.copy()

# Add errors to training predictions (fewer errors)
error_indices_train = np.random.choice(n_samples, size=int(0.08 * n_samples), replace=False)
for idx in error_indices_train:
    # Most errors are to adjacent classes
    if np.random.random() < 0.7:
        y_pred_train[idx] = (y_true[idx] + np.random.choice([-1, 1])) % n_classes
    else:
        y_pred_train[idx] = np.random.randint(0, n_classes)

# Add errors to validation predictions (more errors)
error_indices_val = np.random.choice(n_samples, size=int(0.15 * n_samples), replace=False)
for idx in error_indices_val:
    if np.random.random() < 0.7:
        y_pred_val[idx] = (y_true[idx] + np.random.choice([-1, 1])) % n_classes
    else:
        y_pred_val[idx] = np.random.randint(0, n_classes)

# Calculate confusion matrices
cm_train = confusion_matrix(y_true, y_pred_train)
cm_val = confusion_matrix(y_true, y_pred_val)

# Normalize confusion matrices
cm_train_norm = cm_train.astype('float') / cm_train.sum(axis=1)[:, np.newaxis]
cm_val_norm = cm_val.astype('float') / cm_val.sum(axis=1)[:, np.newaxis]

# Class names (customize based on your problem)
class_names = ['Class A', 'Class B', 'Class C', 'Class D']

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

# Plot Training Confusion Matrix
sns.heatmap(cm_train_norm, annot=True, fmt='.2f', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names, 
            cbar_kws={'label': 'Proportion'}, ax=ax1,
            annot_kws={'fontsize': 11, 'fontweight': 'bold'})
ax1.set_xlabel('Predicted Label', fontsize=14, fontweight='bold')
ax1.set_ylabel('True Label', fontsize=14, fontweight='bold')
ax1.set_title('Training Confusion Matrix', fontsize=16, fontweight='bold', pad=20)
ax1.tick_params(axis='both', which='major', labelsize=12)

# Plot Validation Confusion Matrix
sns.heatmap(cm_val_norm, annot=True, fmt='.2f', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names, 
            cbar_kws={'label': 'Proportion'}, ax=ax2,
            annot_kws={'fontsize': 11, 'fontweight': 'bold'})
ax2.set_xlabel('Predicted Label', fontsize=14, fontweight='bold')
ax2.set_ylabel('True Label', fontsize=14, fontweight='bold')
ax2.set_title('Validation Confusion Matrix', fontsize=16, fontweight='bold', pad=20)
ax2.tick_params(axis='both', which='major', labelsize=12)

plt.suptitle('Normalized Confusion Matrices', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('confusion_matrices_paper.png', dpi=300, bbox_inches='tight')
plt.savefig('confusion_matrices_paper.pdf', dpi=300, bbox_inches='tight')
plt.close()

# Create a single confusion matrix with absolute values
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

# Use validation data for single matrix
sns.heatmap(cm_val, annot=True, fmt='d', cmap='YlOrRd', 
            xticklabels=class_names, yticklabels=class_names, 
            cbar_kws={'label': 'Count'}, ax=ax,
            annot_kws={'fontsize': 12, 'fontweight': 'bold'})
ax.set_xlabel('Predicted Label', fontsize=14, fontweight='bold')
ax.set_ylabel('True Label', fontsize=14, fontweight='bold')
ax.set_title('Validation Confusion Matrix (Absolute Values)', fontsize=16, fontweight='bold', pad=20)
ax.tick_params(axis='both', which='major', labelsize=12)

plt.tight_layout()
plt.savefig('confusion_matrix_absolute_paper.png', dpi=300, bbox_inches='tight')
plt.savefig('confusion_matrix_absolute_paper.pdf', dpi=300, bbox_inches='tight')
plt.close()

# Calculate and print metrics from confusion matrix
def calculate_metrics(cm, class_names):
    """Calculate precision, recall, and F1 for each class"""
    n_classes = cm.shape[0]
    precision = np.zeros(n_classes)
    recall = np.zeros(n_classes)
    f1 = np.zeros(n_classes)
    
    for i in range(n_classes):
        # Precision: TP / (TP + FP)
        precision[i] = cm[i, i] / cm[:, i].sum() if cm[:, i].sum() > 0 else 0
        # Recall: TP / (TP + FN)
        recall[i] = cm[i, i] / cm[i, :].sum() if cm[i, :].sum() > 0 else 0
        # F1: 2 * (precision * recall) / (precision + recall)
        f1[i] = 2 * (precision[i] * recall[i]) / (precision[i] + recall[i]) if (precision[i] + recall[i]) > 0 else 0
    
    print("\nPer-Class Metrics:")
    print("-" * 60)
    print(f"{'Class':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
    print("-" * 60)
    for i, name in enumerate(class_names):
        print(f"{name:<12} {precision[i]:<12.3f} {recall[i]:<12.3f} {f1[i]:<12.3f}")
    
    # Overall accuracy
    accuracy = np.diag(cm).sum() / cm.sum()
    print(f"\nOverall Accuracy: {accuracy:.3f}")
    
    return precision, recall, f1, accuracy

print("\nTraining Metrics:")
print("=" * 60)
train_metrics = calculate_metrics(cm_train, class_names)

print("\n\nValidation Metrics:")
print("=" * 60)
val_metrics = calculate_metrics(cm_val, class_names)

print("\n\nGenerated files:")
print("1. confusion_matrices_paper.png/pdf (Normalized, side-by-side)")
print("2. confusion_matrix_absolute_paper.png/pdf (Absolute values)")