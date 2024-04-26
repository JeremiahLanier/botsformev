class FeatureToggle:
    def __init__(self):
        self.features = {}

    def set_feature(self, feature_name, status):
        self.features[feature_name] = status

    def is_enabled(self, feature_name):
        return self.features.get(feature_name, False)
