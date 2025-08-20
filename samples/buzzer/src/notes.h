/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef __NOTES_H__
#define __NOTES_H__

/* pitches in Hz */
typedef enum {
	A0 = 28,  /* 27.5000 Hz (A'') */
	As0 = 29, /* 29.1352 Hz (Ais''/B'') */
	Bb0 = As0,
	B0 = 31, /* 30.8677 Hz (H'') */
	H0 = B0,

	C1 = 33,  /* 32.7032 Hz (C') */
	Cs1 = 35, /* 34.6478 Hz (Cis'/Des') */
	Db1 = Cs1,
	D1 = 37,  /* 36.7081 Hz (D') */
	Ds1 = 39, /* 38.8909 Hz (Dis'/Es') */
	Eb1 = Ds1,
	E1 = 41,  /* 41.2034 Hz (E') */
	F1 = 44,  /* 43.6535 Hz (F') */
	Fs1 = 46, /* 46.2493 Hz (Fis'/Ges') */
	Gb1 = Fs1,
	G1 = 49,  /* 48.9994 Hz (G') */
	Gs1 = 52, /* 51.9131 Hz (Gis'/As') */
	Ab1 = Gs1,
	A1 = 55,  /* 55.0000 Hz (A') */
	As1 = 58, /* 58.2705 Hz (Ais'/B') */
	Bb1 = As1,
	B1 = 62, /* 61.7354 Hz (H') */
	H1 = B1,

	C2 = 65,  /* 65.4064 Hz (C) */
	Cs2 = 69, /* 69.2957 Hz (Cis/Des) */
	Db2 = Cs2,
	D2 = 73,  /* 73.4162 Hz (D) */
	Ds2 = 78, /* 77.7817 Hz (Dis/Es) */
	Eb2 = Ds2,
	E2 = 82,  /* 82.4069 Hz (E) */
	F2 = 87,  /* 87.3071 Hz (F) */
	Fs2 = 93, /* 92.4986 Hz (Fis/Ges) */
	Gb2 = Fs2,
	G2 = 98,   /* 97.9989 Hz (G) */
	Gs2 = 104, /* 103.826 Hz (Gis/As) */
	Ab2 = Gs2,
	A2 = 110,  /* 110.000 Hz (A) */
	As2 = 117, /* 116.541 Hz (Ais/B) */
	Bb2 = As2,
	B2 = 124, /* 123.471 Hz (H) */
	H2 = B2,

	C3 = 131,  /* 130.813 Hz (c) */
	Cs3 = 139, /* 138.591 Hz (cis/des) */
	Db3 = Cs3,
	D3 = 147,  /* 146.832 Hz (d) */
	Ds3 = 156, /* 155.563 Hz (dis/es) */
	Eb3 = Ds3,
	E3 = 165,  /* 164.814 Hz (e) */
	F3 = 175,  /* 174.614 Hz (f) */
	Fs3 = 185, /* 184.997 Hz (fis/ges) */
	Gb3 = Fs3,
	G3 = 196,  /* 195.998 Hz (g) */
	Gs3 = 208, /* 207.652 Hz (gis/as) */
	Ab3 = Gs3,
	A3 = 220,  /* 220.000 Hz (a) */
	As3 = 233, /* 233.082 Hz (ais/b) */
	Bb3 = As3,
	B3 = 247, /* 246.942 Hz (h) */
	H3 = B3,

	C4 = 262,  /* 261.626 Hz (c') */
	Cs4 = 277, /* 277.183 Hz (cis'/des') */
	Db4 = Cs4,
	D4 = 294,  /* 293.665 Hz (d') */
	Ds4 = 311, /* 311.127 Hz (dis'/es') */
	Eb4 = Ds4,
	E4 = 330,  /* 329.628 Hz (e') */
	F4 = 349,  /* 349.228 Hz (f') */
	Fs4 = 370, /* 369.994 Hz (fis'/ges') */
	Gb4 = Fs4,
	G4 = 392,  /* 391.995 Hz (g') */
	Gs4 = 415, /* 415.305 Hz (gis'/as') */
	Ab4 = Gs4,
	A4 = 440,  /* 440.000 Hz (a') - concert pitch */
	As4 = 466, /* 466.164 Hz (ais'/b') */
	Bb4 = As4,
	B4 = 494, /* 493.883 Hz (h') */
	H4 = B4,

	C5 = 523,  /* 523.251 Hz (c'') */
	Cs5 = 554, /* 554.365 Hz (cis''/des'') */
	Db5 = Cs5,
	D5 = 587,  /* 587.330 Hz (d'') */
	Ds5 = 622, /* 622.254 Hz (dis''/es'') */
	Eb5 = Ds5,
	E5 = 659,  /* 659.255 Hz (e'') */
	F5 = 699,  /* 698.456 Hz (f'') */
	Fs5 = 740, /* 739.989 Hz (fis''/ges'') */
	Gb5 = Fs5,
	G5 = 784,  /* 783.991 Hz (g'') */
	Gs5 = 831, /* 830.609 Hz (gis''/as'') */
	Ab5 = Gs5,
	A5 = 880,  /* 880.000 Hz (a'') */
	As5 = 932, /* 932.328 Hz (ais''/b'') */
	Bb5 = As5,
	B5 = 988, /* 987.767 Hz (h'') */
	H5 = B5,

	C6 = 1046,  /* 1046.50 Hz (c''') */
	Cs6 = 1109, /* 1108.73 Hz (cis'''/des''') */
	Db6 = Cs6,
	D6 = 1175,  /* 1174.66 Hz (d''') */
	Ds6 = 1245, /* 1244.51 Hz (dis'''/es''') */
	Eb6 = Ds6,
	E6 = 1319,  /* 1318.51 Hz (e''') */
	F6 = 1397,  /* 1396.91 Hz (f''') */
	Fs6 = 1480, /* 1479.98 Hz (fis'''/ges''') */
	Gb6 = Fs6,
	G6 = 1568,  /* 1567.98 Hz (g''') */
	Gs6 = 1661, /* 1661.22 Hz (gis'''/as''') */
	Ab6 = Gs6,
	A6 = 1760,  /* 1760.00 Hz (a''') */
	As6 = 1865, /* 1864.66 Hz (ais'''/b''') */
	Bb6 = As6,
	B6 = 1976, /* 1975.53 Hz (h''') */
	H6 = B6,

	C7 = 2093,  /* 2093,00 Hz (c'''') */
	Cs7 = 2218, /* 2217,46 Hz (cis''''/des'''') */
	Db7 = Cs7,
	D7 = 2349,  /* 2349,32 Hz (d'''') */
	Ds7 = 2489, /* 2489,02 Hz (dis''''/es'''') */
	Eb7 = Ds7,
	E7 = 2637,  /* 2637,02 Hz (e'''') */
	F7 = 2794,  /* 2793,83 Hz (f'''') */
	Fs7 = 2960, /* 2959,96 Hz (fis''''/ges'''') */
	Gb7 = Fs7,
	G7 = 3136,  /* 3135,96 Hz (g'''') */
	Gs7 = 3322, /* 3322,44 Hz (gis''''/as'''') */
	Ab7 = Gs7,
	A7 = 3520,  /* 3520,00 Hz (a'''') */
	As7 = 3729, /* 3729,31 Hz (ais''''/b'''') */
	Bb7 = As7,
	B7 = 3951, /* 3951,07 Hz (h'''') */
	H7 = B7,

	C8 = 4186, /* 4186,01 Hz (c''''') */

	REST = 1,
} note_pitch_t;

/* duration in msec */
typedef enum {
	sixtyfourth = 9,
	thirtytwoth = 19,
	sixteenth = 38,
	ninth = 50, /* unusually */
	eighth = 75,
	sixth = 100, /* unusually */
	quarter = 150,
	third = 200, /* unusually */
	half = 300,
	whole = 600,
} note_duration_t;

typedef struct {
	note_pitch_t pitch;       /* Hz */
	note_duration_t duration; /* msec */
} note_t;

#endif /* __NOTES_H__ */
