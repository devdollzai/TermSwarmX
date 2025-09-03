class DataProcessor:
    """
    A simple data processing class.
    """
    
    def __init__(self, data):
        self.data = data
        self.processed = False
    
    def process(self):
        """Process the data."""
        if not self.processed:
            self.data = [x * 2 for x in self.data]
            self.processed = True
        return self.data
    
    def get_summary(self):
        """Get a summary of the data."""
        return {
            'count': len(self.data),
            'sum': sum(self.data),
            'processed': self.processed
        }

# Example usage
if __name__ == "__main__":
    processor = DataProcessor([1, 2, 3, 4, 5])
    print(f"Original: {processor.data}")
    processed = processor.process()
    print(f"Processed: {processed}")
    print(f"Summary: {processor.get_summary()}")
