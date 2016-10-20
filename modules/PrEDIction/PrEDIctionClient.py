class PrEDIctionClient:

    def __init__(self):
        self.client = None

    def set_client(self, client):
        self.client = client

    def clean(self):
        self.client = None
        
    def get_desc(self):
        if self.client[0] is None:
            self.client[0] = 'none'
            
        return '\''+self.client[0]+'\''

    def get_document_type(self):
        if self.client[1] is None:
            self.client[1] = 'none'

        return '\''+self.client[1]+'\''
    
    def get_id(self):
        if self.client[0] is None:
            self.client[0] = 'none'
        if self.client[1] is None:
            self.client[1] = 'none'

        return self.client[0] + '_' + self.client[1]

    def get_count(self):
        return self.client[2]
