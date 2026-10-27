"""
Flask Web Server for Breast Cancer 3D Bio-Cyber Lab
Dynamic Model Training & 3D Interactive Visualization
Runs locally at http://localhost:5000
"""

import sys
import os
import math
import json

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, send_from_directory, jsonify, request
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = Flask(__name__, static_folder='.', static_url_path='')

# Load Breast Cancer Wisconsin dataset
data = load_breast_cancer()
# 0: radius, 1: texture, 6: concavity
X = data.data[:, [0, 1, 6]]
y = data.target

# Global model state
state = {
    'test_size': 0.2,
    'random_state': 42,
    'max_depth': 4,
    'n_estimators': 15,
    'k': 7,
    'dt_model': None,
    'knn_model': None,
    'rf_model': None,
    'idx_train': [],
    'idx_test': []
}

def train_all_models():
    indices = list(range(len(y)))
    idx_tr, idx_te = train_test_split(
        indices, 
        test_size=state['test_size'], 
        random_state=state['random_state']
    )
    state['idx_train'] = idx_tr
    state['idx_test'] = idx_te

    X_train, X_test = X[idx_tr], X[idx_te]
    y_train, y_test = y[idx_tr], y[idx_te]

    dt = DecisionTreeClassifier(
        max_depth=state['max_depth'], 
        random_state=state['random_state']
    ).fit(X_train, y_train)

    knn = KNeighborsClassifier(
        n_neighbors=state['k']
    ).fit(X_train, y_train)

    rf = RandomForestClassifier(
        n_estimators=state['n_estimators'], 
        max_depth=state['max_depth'], 
        random_state=state['random_state']
    ).fit(X_train, y_train)

    state['dt_model'] = dt
    state['knn_model'] = knn
    state['rf_model'] = rf

    dt_acc = round(float(accuracy_score(y_test, dt.predict(X_test))) * 100, 1)
    knn_acc = round(float(accuracy_score(y_test, knn.predict(X_test))) * 100, 1)
    rf_acc = round(float(accuracy_score(y_test, rf.predict(X_test))) * 100, 1)

    # 3D Decision Tree Graph Extraction
    nodes = []
    links = []
    splits = []
    feat_names = ['radius', 'texture', 'concavity']

    def traverse(node, depth, x, y_pos, spread, parent_id):
        is_leaf = bool(dt.tree_.children_left[node] == _tree.TREE_LEAF)
        val = dt.tree_.value[node][0]
        total = float(val.sum())
        prob_m = round(float(val[0] / total), 3)
        prob_b = round(float(val[1] / total), 3)

        node_obj = {
            'id': int(node),
            'parent_id': parent_id,
            'depth': depth,
            'is_leaf': is_leaf,
            'x': round(x, 2),
            'y': round(y_pos, 2),
            'z': 0,
            'samples': int(total),
            'prob_malignant': prob_m,
            'prob_benign': prob_b,
            'prediction': 1 if prob_b >= 0.5 else 0
        }

        if not is_leaf:
            f_idx = int(dt.tree_.feature[node])
            thresh = round(float(dt.tree_.threshold[node]), 3)
            node_obj['feature'] = feat_names[f_idx]
            node_obj['feature_idx'] = f_idx
            node_obj['threshold'] = thresh

            splits.append({'feature_idx': f_idx, 'threshold': thresh})

            left_child = int(dt.tree_.children_left[node])
            right_child = int(dt.tree_.children_right[node])

            node_obj['left_id'] = left_child
            node_obj['right_id'] = right_child
            nodes.append(node_obj)

            dy = 10
            next_spread = spread * 0.52

            links.append({
                'source': int(node),
                'target': left_child,
                'type': 'left',
                'source_pos': [round(x, 2), round(y_pos, 2), 0],
                'target_pos': [round(x - spread, 2), round(y_pos - dy, 2), 0]
            })
            traverse(left_child, depth + 1, x - spread, y_pos - dy, next_spread, int(node))

            links.append({
                'source': int(node),
                'target': right_child,
                'type': 'right',
                'source_pos': [round(x, 2), round(y_pos, 2), 0],
                'target_pos': [round(x + spread, 2), round(y_pos - dy, 2), 0]
            })
            traverse(right_child, depth + 1, x + spread, y_pos - dy, next_spread, int(node))
        else:
            nodes.append(node_obj)

    traverse(0, 0, 0, 26, 22, None)

    # 3D Random Forest Constellation Coordinates
    rf_constellation = []
    n_est = state['n_estimators']
    for i in range(n_est):
        angle = (2 * math.pi * i) / n_est
        R = 30
        cx = round(R * math.cos(angle), 2)
        cz = round(R * math.sin(angle), 2)
        cy = round(5 * math.sin(2 * angle), 2)
        rf_constellation.append({
            'tree_id': i,
            'pos': [cx, cy, cz],
            'angle': round(angle, 3)
        })

    return {
        'dt_acc': dt_acc,
        'knn_acc': knn_acc,
        'rf_acc': rf_acc,
        'train_samples': len(idx_tr),
        'test_samples': len(idx_te),
        'test_indices': [int(i) for i in idx_te],
        'dt_nodes': nodes,
        'dt_links': links,
        'dt_splits': splits,
        'rf_constellation': rf_constellation,
        'rf_importances': [round(float(v) * 100, 1) for v in rf.feature_importances_]
    }

# Initial model training
init_meta = train_all_models()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/get_initial_data', methods=['GET'])
def get_initial_data():
    dataset = []
    for i in range(len(y)):
        dataset.append([
            round(float(X[i, 0]), 2),
            round(float(X[i, 1]), 2),
            round(float(X[i, 2]), 4),
            int(y[i])
        ])

    stats = {
        'min': [float(X[:, 0].min()), float(X[:, 1].min()), float(X[:, 2].min())],
        'max': [float(X[:, 0].max()), float(X[:, 1].max()), float(X[:, 2].max())],
        'dt_acc': init_meta['dt_acc'],
        'knn_acc': init_meta['knn_acc'],
        'rf_acc': init_meta['rf_acc'],
        'train_samples': init_meta['train_samples'],
        'test_samples': init_meta['test_samples'],
        'rf_importances': init_meta['rf_importances']
    }

    return jsonify({
        'dataset': dataset,
        'stats': stats,
        'meta': init_meta,
        'params': {
            'test_size': state['test_size'],
            'random_state': state['random_state'],
            'max_depth': state['max_depth'],
            'n_estimators': state['n_estimators'],
            'k': state['k']
        }
    })

@app.route('/api/retrain', methods=['POST'])
def retrain():
    req = request.json or {}
    if 'test_size' in req:
        state['test_size'] = float(req['test_size'])
    if 'random_state' in req:
        state['random_state'] = int(req['random_state'])
    if 'max_depth' in req:
        state['max_depth'] = max(1, min(10, int(req['max_depth'])))
    if 'n_estimators' in req:
        state['n_estimators'] = max(3, min(40, int(req['n_estimators'])))
    if 'k' in req:
        state['k'] = max(1, min(31, int(req['k'])))

    res = train_all_models()
    return jsonify({
        'success': True,
        'meta': res,
        'params': {
            'test_size': state['test_size'],
            'random_state': state['random_state'],
            'max_depth': state['max_depth'],
            'n_estimators': state['n_estimators'],
            'k': state['k']
        }
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    req = request.json or {}
    r = float(req.get('radius', 14.1))
    t = float(req.get('texture', 19.3))
    c = float(req.get('concavity', 0.089))
    sample = [[r, t, c]]

    # 1. Decision Tree Path
    dt = state['dt_model']
    dt_pred = int(dt.predict(sample)[0])
    dt_prob = [float(p) for p in dt.predict_proba(sample)[0]]

    # Traverse DT to find active path of node IDs
    active_path_ids = []
    active_path_steps = []
    curr_node = 0
    feat_names = ['radius', 'texture', 'concavity']
    val_map = {'radius': r, 'texture': t, 'concavity': c}

    while True:
        active_path_ids.append(curr_node)
        if dt.tree_.children_left[curr_node] == _tree.TREE_LEAF:
            break
        f_idx = dt.tree_.feature[curr_node]
        f_name = feat_names[f_idx]
        val = val_map[f_name]
        thresh = float(dt.tree_.threshold[curr_node])
        goes_left = bool(val <= thresh)

        active_path_steps.append({
            'node_id': curr_node,
            'feature': f_name,
            'value': round(val, 2),
            'threshold': round(thresh, 3),
            'goes_left': goes_left
        })

        if goes_left:
            curr_node = int(dt.tree_.children_left[curr_node])
        else:
            curr_node = int(dt.tree_.children_right[curr_node])

    # 2. Random Forest Tree Votes
    rf = state['rf_model']
    rf_pred = int(rf.predict(sample)[0])
    rf_prob = [float(p) for p in rf.predict_proba(sample)[0]]

    rf_votes = []
    for i, est in enumerate(rf.estimators_):
        p = int(est.predict(sample)[0])
        rf_votes.append({
            'tree_id': i,
            'vote': p # 1 = benign, 0 = malignant
        })

    # 3. KNN Prediction
    knn = state['knn_model']
    knn_pred = int(knn.predict(sample)[0])
    knn_prob = [float(p) for p in knn.predict_proba(sample)[0]]

    return jsonify({
        'dt': {
            'prediction': dt_pred,
            'prob_benign': round(dt_prob[1], 3),
            'prob_malignant': round(dt_prob[0], 3),
            'active_path_ids': active_path_ids,
            'steps': active_path_steps
        },
        'rf': {
            'prediction': rf_pred,
            'prob_benign': round(rf_prob[1], 3),
            'prob_malignant': round(rf_prob[0], 3),
            'votes': rf_votes,
            'votes_benign': sum(1 for v in rf_votes if v['vote'] == 1),
            'votes_malignant': sum(1 for v in rf_votes if v['vote'] == 0)
        },
        'knn': {
            'prediction': knn_pred,
            'prob_benign': round(knn_prob[1], 3),
            'prob_malignant': round(knn_prob[0], 3)
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 60)
    print("BIO-CYBER 3D ONCOLOGY LAB SERVER RUNNING!")
    print(f"Open in browser: http://localhost:{port}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
