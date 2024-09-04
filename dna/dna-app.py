######################
# Import libraries
######################

import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

######################
# Page Title
######################

# Load and display the DNA logo

image = Image.open('dna/dna-logo.jpg')
st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

***
""")

######################
# Input Text Box
######################

st.header('Enter DNA sequence')

# Default sequence input
sequence_input = """>DNA Query 2
GAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG
ATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC
TGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT
HHH"""

# Display input box for DNA sequence
sequence = st.text_area("Sequence input", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:]  # Skips the sequence name (first line)
sequence = ''.join(sequence)  # Concatenates list to string

st.write("""
***
""")

## Prints the input DNA sequence
st.header('INPUT (DNA Query)')
st.write(sequence)

## DNA nucleotide count function
def DNA_nucleotide_count(seq):
    """
    Function to count nucleotides and any other characters in a given DNA sequence.
    """
    unique_characters = set(seq)  # Get all unique characters in the sequence
    counts = {char: seq.count(char) for char in unique_characters}  # Count each character
    return counts

# Get nucleotide counts including any extra characters
nucleotide_counts = DNA_nucleotide_count(sequence)

######################
# Display Output
######################

st.header('OUTPUT (DNA Nucleotide Count)')

### 1. Print dictionary of nucleotide counts
st.subheader('1. Print dictionary')
st.write(nucleotide_counts)

### 2. Print nucleotide counts as text
st.subheader('2. Print text')
for nucleotide, count in nucleotide_counts.items():
    st.write(f"There are {count} {nucleotide} (count of '{nucleotide}')")

### 3. Display DataFrame
st.subheader('3. Display DataFrame')
df = pd.DataFrame.from_dict(nucleotide_counts, orient='index', columns=['count'])
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'nucleotide'})
st.write(df)

### 4. Display Bar Chart using Altair
st.subheader('4. Display Bar chart')
chart = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
).properties(
    width=alt.Step(80)  # controls width of bar.
)
st.altair_chart(chart)
