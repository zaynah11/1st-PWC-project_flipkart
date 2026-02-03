import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

def load_environment_variables():
    load_dotenv()
    return {
        'host': os.getenv('db_host'),
        'port': os.getenv('db_port'),
        'database': os.getenv('db_name'),
        'user': os.getenv('db_user'),
        'password': os.getenv('db_password'),
    }

def create_db_engine(config):
    connection_string = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    return create_engine(connection_string)

def load_data(engine, query='SELECT * FROM final_table'):
    return pd.read_sql(query, engine)

def calculate_performance(df):
    performance = df.groupby('call_center').agg({
        'csat_score': 'mean',
        'call_duration_in_minutes': 'mean',
    }).reset_index().rename(columns={
        'csat_score': 'avg_csat_score',
        'call_duration_in_minutes': 'avg_call_duration',
    })
    performance.to_csv('performance_by_call_center.csv', index=False)
    return performance

def count_queries_by_center_and_reason(df):
    query_counts = df.groupby(['call_center', 'reason']).size().reset_index(name='count')
    query_counts.to_csv('query_counts_by_center_and_reason.csv', index=False)
    return query_counts

def pivot_query_counts(query_counts):
    pivot = query_counts.pivot(index='call_center', columns='reason', values='count').fillna(0)
    pivot.to_csv('pivot_query_counts.csv')
    return pivot

def summarize_query_performance(df):
    summary = df.groupby(['call_center', 'reason']).agg(
        query_count=pd.NamedAgg(column='reason', aggfunc='count'),
        avg_csat_score=pd.NamedAgg(column='csat_score', aggfunc='mean')
    ).reset_index()
    summary.to_csv('query_summary.csv', index=False)
    return summary

def pivot_summary_counts_and_csat(summary):
    pivot_count = summary.pivot(index='call_center', columns='reason', values='query_count').fillna(0)
    pivot_csat = summary.pivot(index='call_center', columns='reason', values='avg_csat_score').fillna(0)
    pivot_count.to_csv('pivot_query_count.csv')
    pivot_csat.to_csv('pivot_avg_csat_score.csv')
    return pivot_count, pivot_csat

def average_csat_per_query(df):
    avg_csat = df.groupby('reason')['csat_score'].mean().reset_index().rename(columns={'csat_score': 'avg_csat_score'})
    avg_csat.to_csv('avg_csat_per_query.csv', index=False)
    return avg_csat

def response_time_analysis(df):
    response_counts = df.groupby(['call_center', 'response_time']).size().reset_index(name='count')
    pivot_resp = response_counts.pivot(index='call_center', columns='response_time', values='count').fillna(0)
    pivot_resp.to_csv('pivot_response_time_counts.csv')

    total_calls = df.groupby('call_center').size().reset_index(name='total')
    response_counts = response_counts.merge(total_calls, on='call_center')
    response_counts['percent'] = (response_counts['count'] / response_counts['total']) * 100

    response_counts.to_csv('response_time_counts_and_percent.csv', index=False)
    return response_counts, pivot_resp

def main():
    config = load_environment_variables()
    engine = create_db_engine(config)

    df = load_data(engine)

    print("Calculating performance metrics...")
    performance = calculate_performance(df)

    print("Counting queries by call center and reason...")
    query_counts = count_queries_by_center_and_reason(df)

    print("Pivoting query counts...")
    pivot_query_counts(query_counts)

    print("Summarizing query performance...")
    query_summary = summarize_query_performance(df)

    print("Pivoting query summary counts and CSAT scores...")
    pivot_summary_counts_and_csat(query_summary)

    print("Calculating average CSAT per query reason...")
    average_csat_per_query(df)

    print("Analyzing response times...")
    response_time_analysis(df)

    print("All analysis complete. CSV files saved.")

if __name__ == "__main__":
    main()