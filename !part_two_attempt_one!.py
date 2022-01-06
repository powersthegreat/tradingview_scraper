import pandas as pandas
from collections import defaultdict

oscillators_df = pandas.read_excel("market-movers-large-cap.xlsx", sheet_name = 7)

tickers = oscillators_df['TickerNo matches']
adx = oscillators_df['ADX']
ao = oscillators_df['AO']
atr = oscillators_df['ATR']
cci20 = oscillators_df['CCI20']
macd_level = oscillators_df['MACD Level']
macd_signal = oscillators_df['MACD Signal']
mom = oscillators_df['MOM']
rsi_14 = oscillators_df['RSI14']
stoch_k = oscillators_df['Stoch %K']
stoch_d = oscillators_df['Stoch %D']

ticker_list = []
counter_list = []
index_list = []
full_oscillators_list = []

for ticker in tickers:
    ticker_list.append(ticker)

for i in range(0, len(ticker_list)):
    counter_list.append(0)
    index_list.append(i)

ticker_count_dict = dict(zip(index_list,counter_list))

adx_list = []
for values in adx:
    adx_list.append(values[-1])
full_oscillators_list.append(adx_list)

ao_list = []
for values in ao:
    ao_list.append(values[-1])
full_oscillators_list.append(ao_list)

atr_list = []
for values in ao:
    atr_list.append(values[-1])
full_oscillators_list.append(atr_list)

cci20_list = []
for values in ao:
    cci20_list.append(values[-1])
full_oscillators_list.append(cci20_list)

macd_level_list = []
for values in ao:
    macd_level_list.append(values[-1])
full_oscillators_list.append(macd_level_list)

mom_list = []
for values in ao:
    mom_list.append(values[-1])
full_oscillators_list.append(mom_list)

rsi_14_list = []
for values in ao:
    rsi_14_list.append(values[-1])
full_oscillators_list.append(rsi_14_list)

stoch_k_list = []
for values in ao:
    stoch_k_list.append(values[-1])
full_oscillators_list.append(stoch_k_list)

tickers_readings_list = [[] for _ in range(0,100)]


index_counter = -1
for values in adx:
    index_counter +=1
    tickers_readings_list[index_counter].append(values[-1])

index_counter_two = -1
for values in ao:
    index_counter_two += 1
    tickers_readings_list[index_counter_two].append(values[-1])

index_counter_four = -1
for values in cci20:
    index_counter_four += 1
    tickers_readings_list[index_counter_four].append(values[-1])

index_counter_five = -1
for values in macd_level:
    index_counter_five += 1
    tickers_readings_list[index_counter_five].append(values[-1])

index_counter_six = -1
for values in mom:
    index_counter_six += 1
    tickers_readings_list[index_counter_six].append(values[-1])

index_counter_seven = -1
for values in rsi_14:
    index_counter_seven += 1
    tickers_readings_list[index_counter_seven].append(values[-1])

index_counter_eight = -1
for values in stoch_k:
    index_counter_eight += 1
    tickers_readings_list[index_counter_eight].append(values[-1])

ticker_list_2 = []
for ticker in ticker_list:
    good = ticker.split('D')[0]
    ticker_list_2.append(good)

tickers_readings_dict = dict(zip(ticker_list_2, tickers_readings_list))

buy_signals_count = []

for sub_lists in tickers_readings_dict.values():
    cnt = sub_lists.count('B')
    buy_signals_count.append(cnt)

    
final_dict = dict(zip(ticker_list_2, buy_signals_count))

marklist = sorted(final_dict.items(), key=lambda x:x[1], reverse = True)
sortdict = dict(marklist)
print(sortdict)



