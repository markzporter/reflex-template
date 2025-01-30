import reflex as rx
class DashApp(rx.Model):
    app_name: str 
    url: str 
    service_id: str 
    created_at: str 
    deployment_status: str 
    