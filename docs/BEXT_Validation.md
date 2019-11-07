## BAroQUe BEXT Validation

Module used: wav_bext_chunk_validation.py

BAroQUe performs the following checks on each WAVE file:

  - Each WAV file must have a BEXT chunk.
  - Must have "Description" field.
  - "Description" value must match CSV "Item Title" value.
  - Must have "Originator" field.
  - "Originator" field must be "US, MiU-H"
  - Must have "Originator Reference" field.
  - "Originator" field must match the MiU-H_Filename (without Extension) convention.
  - Must have "OriginationDate" field.
  - "OriginationDate" field must use the YYYY-MM-DD convention.
  - Must have "TimeReference" field.
  - Must have "Origination time" field.
  - "Origination time" field must use the HH:mm:ss convention.
  - Must have "Coding History" field.
  - "Coding History" field may only use appropriate, comma-separated codes (A=, F=, B=, W=, M=, T=)
  - "Coding History" field must have at least one A field.
  - "Coding History" field A must be "ANALOG" or "PCM."
  - "Coding History" field must have at least one F field.
  - If there's a "Coding History" field F field, it must be 9600.
  - "Coding History" field may have B field.
  - "Coding History" field may have W field. if exists it should be 24
  - "Coding History" field must have M field.
  - "Coding History" field must have T field.
