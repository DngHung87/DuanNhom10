import pandas as pd


class QuanLyTK:
    def __init__(self, file_path, title=[]):
        self.file_path = file_path
        self.title = title

    def checkLogin(self, username, password):
        data = pd.read_csv(self.file_path)
        user = data[(data['username'] == username) & (data['password'] == password)]
        return not user.empty

    def list(self, page=1, page_size=100):
        data = pd.read_csv(self.file_path)
        return data.to_dict('records')

    def create(self, new_data):
        data = pd.read_csv(self.file_path)
        new_row = pd.DataFrame([new_data], columns=self.title)
        data = pd.concat([data, new_row], ignore_index=True)
        data.to_csv(self.file_path, index=False)
        return True

    def delete(self, title_keyword, keyword):
        data = pd.read_csv(self.file_path)
        result = data[~data[title_keyword].astype(str).str.contains(keyword)]
        result.to_csv(self.file_path, index=False)
        return True

    def update(self, title_keyword, keyword, title_edit=[], new_data=[]):
        data = pd.read_csv(self.file_path)
        for i, col in enumerate(title_edit):
            data.loc[data[title_keyword].astype(str) == keyword, col] = new_data[i]
        data.to_csv(self.file_path, index=False)
        return True
