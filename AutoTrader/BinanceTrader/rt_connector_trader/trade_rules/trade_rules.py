import pandas as pd


def message_handler(message):
    print(message, "\ntype : ", type(message))


class GetData():
    def __init__(self):
        self.df_dict = dict() # keys : markPriceUpdate, aggTrade

    def event_2_DataFrame(self, message):
        
        try:
            eventType = message['data']['e']
            event = message['data']
        except:
            try:
                eventType = message['e']
                event = message
            except:
                message_handler(message)
                return

        try:
            df_data = self.df_dict[eventType]
        except:
            df_data = pd.DataFrame()
            
        message_df = pd.DataFrame(event, index=[0])
        res_df = pd.concat([df_data, message_df], axis=0)
        res_df.reset_index(drop=True, inplace=True)

        self.df_dict[eventType] = res_df