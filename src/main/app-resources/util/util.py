#!/opt/anaconda/envs/env_ewf_satcen_03_01_01/bin/python

import cioppy

ciop = cioppy.Cioppy()

def log_input(reference):
    """
    Just logs the input reference, using the ciop.log function
    """

    ciop.log('INFO', 'processing input: ' + reference)
    
def pass_next_node(input):
    """
    Pass the input reference to the next node as is, without storing it on HDFS
    """

    ciop.publish(input, mode='silent')

def group_analysis(df):
    df['ordinal_type'] = 'NaN'
    slave_date=df['startdate'].min()[:10]
    master_date=df['startdate'].max()[:10]
    for i in range(len(df)):
    
        if slave_date == df.iloc[i]['startdate'][:10]:
            df.loc[i,'ordinal_type']='Pre'
    
        elif master_date == df.iloc[i]['startdate'][:10]:
            df.loc[i,'ordinal_type']='Pst'

    return 