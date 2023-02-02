import numpy as np
import pandas as pd


def message_handler(message):
    print(message, "\ntype : ", type(message))


class DataCollector():
    def __init__(self):
        self.df_dict = dict() # keys : markPriceUpdate, aggTrade, ...
        self.cut_th = {
            'aggTrade':400,
            'markPrice':1000,
            'kline':1000
        }

    def event_2_DataFrame(self, message):
        
        try:
            eventType = message['data']['e']
            event = message['data']
        except: # when only one stream.
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

        if len(res_df) > self.cut_th[eventType]:
            res_df = res_df[len(res_df)-self.cut_th[eventType]:]

        self.df_dict[eventType] = res_df