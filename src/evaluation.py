from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix


def evaluate_classifier(model, X_test, y_test, name):
    """Return one row of metrics for the model comparison table."""
    y_pred = model.predict(X_test)
    proba = model.predict_proba(X_test)
    binary = proba.shape[1] == 2
    return {
        "model": name,
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred, average="binary" if binary else "weighted"),
        "roc_auc": roc_auc_score(y_test, proba[:, 1]) if binary
                   else roc_auc_score(y_test, proba, multi_class="ovr"),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
    }
