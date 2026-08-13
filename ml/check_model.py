import joblib
model = joblib.load(r"D:\SecurePay-AI\ml\models\fraud_model.pkl")
encoder = joblib.load(r"D:\SecurePay-AI\ml\models\label_encoder.pkl")
# scaler = joblib.load(r"D:\SecurePay-AI\ml\models\scaler.pkl")
feature_columns = joblib.load(r"D:\SecurePay-AI\ml\models\feature_columns.pkl")

print("\n---model---")
print(type(model))
print("\n---encoder---")
print(type(encoder))
print("classes:",encoder.classes_)
# print("\n---scaler---")
# print(type(scaler))
print("\n---feature columns---")
print(type(feature_columns))
for i, feature in enumerate(feature_columns):
    print(i,"->",feature)

print("\n no of features:",len(feature_columns))