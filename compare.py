import json
import csv
import pandas as pd

file1 = 'Google_Result1.json'
file2 = 'hw1.json'
file3 = '100QueriesSet1.txt'


def compare_files(urls1, urls2):
        sum_d_sq = 0
        overlap = 0

            
        for idx2, res2 in enumerate(urls2, start=1):
            if res2 in urls1:
                overlap += 1
                idx1 = urls1.index(res2) + 1
                d = idx1 - idx2
                d_sq = d ** 2
                sum_d_sq += d_sq
                
        return sum_d_sq, overlap
    
    
def get_spearman(sum_d_sq, overlap:int):
    if overlap == 1 and sum_d_sq == 0:
        rho = 1
    elif overlap == 1:
        rho = 0
    elif overlap == 0:
        rho = 0
    else:
        rho = 1 - (6 * sum_d_sq)/(overlap*(overlap  ** 2 - 1))
        
    return rho


# def save_csv(query, overlap, rho, filename='hw1.csv'):
#     with open(filename, 'a', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         percent = overlap * 10
#         writer.writerow([query, overlap, percent, rho])

if __name__ == "__main__":
    df = pd.DataFrame(columns=['Queries', 'Number of Overlapping Results', 'Percent Overlap', 'Spearman Coefficient'])
    
    with open(file3, 'r') as file:
        for line in file:
            query = line.strip()
    # query = 'How do you replace coolant thermostat'
    
            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                    data1 = json.load(f1)
                    data2 = json.load(f2)
                    
                    urls1 = data1[query]
                    urls2 = data2[query]
                    
                    sum_d_sq, overlap = compare_files(urls1, urls2)
                    rho = get_spearman(sum_d_sq, overlap)
                    percent = round((overlap / len(urls2)) * 100)
                    
                    new_row = pd.DataFrame({
                        'Queries': [query],
                        'Number of Overlapping Results': [overlap],
                        'Percent Overlap': [percent],
                        'Spearman Coefficient': [rho]
                    })
                    
                    df = pd.concat([df, new_row], ignore_index=True)
                    
    average = pd.DataFrame({
        'Queries': 'Average',
        'Number of Overlapping Results': [df['Number of Overlapping Results'].mean()],
        'Percent Overlap': [df['Percent Overlap'].mean()],
        'Spearman Coefficient': [df['Spearman Coefficient'].mean()]
    })
                
                
    df = pd.concat([df, average], ignore_index=True)
                    
    df.to_csv('hw1.csv', index=False)
                
                
    
    
    
    
    