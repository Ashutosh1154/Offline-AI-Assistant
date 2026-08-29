import re


def chunk_text(text, chunk_size=1000, overlap=200):

    # Remove unnecessary spaces/newlines
    clean_text = re.sub(r"\s+", " ", text).strip()

    # Split text at sentence boundaries
    sentences = re.split(r"(?<=[.!?])\s+", clean_text)

    chunks = []
    current_sentences = []
    current_length = 0

    for sentence in sentences:

        sentence_length = len(sentence)

        # If adding this sentence makes the chunk too large
        if current_sentences and current_length + sentence_length > chunk_size:

            # Join completed sentences into one chunk
            chunk = " ".join(current_sentences)
            chunks.append(chunk)

            # Keep some previous sentences for overlap
            overlap_sentences = []
            overlap_length = 0

            for previous_sentence in reversed(current_sentences):

                if overlap_length + len(previous_sentence) > overlap:
                    break

                overlap_sentences.insert(0, previous_sentence)
                overlap_length += len(previous_sentence)

            # Start the next chunk with overlapping sentences
            current_sentences = overlap_sentences
            current_length = overlap_length

        current_sentences.append(sentence)
        current_length += sentence_length

    # Add the final remaining chunk
    if current_sentences:
        chunks.append(" ".join(current_sentences))

    return chunks
