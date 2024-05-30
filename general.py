class GeneralFunctions:
    
    # Function to remove words in list a matching list b 
    @staticmethod
    def remove_words_from_list(a, b):
        try:
            modified_list = []
            for item1 in a:
                for word in b:
                    if word in item1:
                        item1 = item1.replace(word, "")
                modified_list.append(item1.strip())  # Strip to remove any leading/trailing spaces
            return modified_list
        except Exception as e:
            print(f"General Function Error Found: {e}")