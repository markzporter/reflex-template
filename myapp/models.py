class DashApp:
    def __init__(self, app_name: str, url: str, id: str, created_at: str):
        self.app_name = app_name
        self.url = url
        self.id = id
        self.created_at = created_at

    def __repr__(self):
        return f"DashApp(name={self.app_name}, url={self.url}, id={self.id}, created_at={self.created_at})"
    
    