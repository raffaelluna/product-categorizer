from datetime import datetime

class BasicLogger:
    def __init__(self):
        pass
    
    def get_time(self):
        
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        
        return self
    
    def log(self, file, message):
        
        self.get_time()
        
        with open(file, "a+") as f:
            f.write(str(self.date) + "-" + str(self.current_time) + "\t\t" + message + "\n")
            
class TrainingLogger(BasicLogger):
    def log_metrics(self, file, metrics_dict):
        
        self.get_time()
        
        with open(file, "a+") as f:
            f.write(f"{self.date}/{self.current_time} - Metrics: {metrics_dict}\n")

class ApiLogger(BasicLogger):
    def log_api(self, file, message):
        
        self.get_time()
        
        with open(file, "a+") as f:
            f.write(f"API: {self.date}/{self.current_time} - {message}\n")
            
class ProcessorLogger(BasicLogger):
    def log_processor(self, file, message):
        
        self.get_time()
        
        with open(file, "a+") as f:
            f.write(f"PREPROCESSOR: {self.date}/{self.current_time} - {message}\n")