/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef __NOTES_H__
#define __NOTES_H__

struct note_duration {
	int note;	/* Hz */
	int duration;	/* msec */
};

/* duration in msec */
#define sixtyfourth 9
#define thirtytwoth 19
#define sixteenth   38
#define ninth       50	/* unusually */
#define eighth      75
#define sixth       100	/* unusually */
#define quarter     150
#define third       200	/* unusually */
#define half        300
#define whole       600

/* notes in Hz */
#define A0  28		/* 27.5000 Hz (A'') */
#define As0 29		/* 29.1352 Hz (Ais''/B'') */
#define Bb0 As0
#define B0  31		/* 30.8677 Hz (H'') */
#define H0  B0

#define C1  33		/* 32.7032 Hz (C') */
#define Cs1 35		/* 34.6478 Hz (Cis'/Des') */
#define Db1 Cs1
#define D1  37		/* 36.7081 Hz (D') */
#define Ds1 39		/* 38.8909 Hz (Dis'/Es') */
#define Eb1 Ds1
#define E1  41		/* 41.2034 Hz (E') */
#define F1  44		/* 43.6535 Hz (F') */
#define Fs1 46		/* 46.2493 Hz (Fis'/Ges') */
#define Gb1 Fs1
#define G1  49		/* 48.9994 Hz (G') */
#define Gs1 52		/* 51.9131 Hz (Gis'/As') */
#define Ab1 Gs1
#define A1  55		/* 55.0000 Hz (A') */
#define As1 58		/* 58.2705 Hz (Ais'/B') */
#define Bb1 As1
#define B1  62		/* 61.7354 Hz (H') */
#define H1  B1

#define C2  65		/* 65.4064 Hz (C) */
#define Cs2 69		/* 69.2957 Hz (Cis/Des) */
#define Db2 Cs2
#define D2  73		/* 73.4162 Hz (D) */
#define Ds2 78		/* 77.7817 Hz (Dis/Es) */
#define Eb2 Ds2
#define E2  82		/* 82.4069 Hz (E) */
#define F2  87		/* 87.3071 Hz (F) */
#define Fs2 93		/* 92.4986 Hz (Fis/Ges) */
#define Gb2 Fs2
#define G2  98		/* 97.9989 Hz (G) */
#define Gs2 104		/* 103.826 Hz (Gis/As) */
#define Ab2 Gs2
#define A2  110		/* 110.000 Hz (A) */
#define As2 117		/* 116.541 Hz (Ais/B) */
#define Bb2 As2
#define B2  124		/* 123.471 Hz (H) */
#define H2  B2

#define C3  131		/* 130.813 Hz (c) */
#define Cs3 139		/* 138.591 Hz (cis/des) */
#define Db3 Cs3
#define D3  147		/* 146.832 Hz (d) */
#define Ds3 156		/* 155.563 Hz (dis/es) */
#define Eb3 Ds3
#define E3  165		/* 164.814 Hz (e) */
#define F3  175		/* 174.614 Hz (f) */
#define Fs3 185		/* 184.997 Hz (fis/ges) */
#define Gb3 Fs3
#define G3  196		/* 195.998 Hz (g) */
#define Gs3 208		/* 207.652 Hz (gis/as) */
#define Ab3 Gs3
#define A3  220		/* 220.000 Hz (a) */
#define As3 233		/* 233.082 Hz (ais/b) */
#define Bb3 As3
#define B3  247		/* 246.942 Hz (h) */
#define H3  B3

#define C4  262		/* 261.626 Hz (c') */
#define Cs4 277		/* 277.183 Hz (cis'/des') */
#define Db4 Cs4
#define D4  294		/* 293.665 Hz (d') */
#define Ds4 311		/* 311.127 Hz (dis'/es') */
#define Eb4 Ds4
#define E4  330		/* 329.628 Hz (e') */
#define F4  349		/* 349.228 Hz (f') */
#define Fs4 370		/* 369.994 Hz (fis'/ges') */
#define Gb4 Fs4
#define G4  392		/* 391.995 Hz (g') */
#define Gs4 415		/* 415.305 Hz (gis'/as') */
#define Ab4 Gs4
#define A4  440		/* 440.000 Hz (a') - concert pitch */
#define As4 466		/* 466.164 Hz (ais'/b') */
#define Bb4 As4
#define B4  494		/* 493.883 Hz (h') */
#define H4  B4

#define C5  523		/* 523.251 Hz (c'') */
#define Cs5 554		/* 554.365 Hz (cis''/des'') */
#define Db5 Cs5
#define D5  587		/* 587.330 Hz (d'') */
#define Ds5 622		/* 622.254 Hz (dis''/es'') */
#define Eb5 Ds5
#define E5  659		/* 659.255 Hz (e'') */
#define F5  699		/* 698.456 Hz (f'') */
#define Fs5 740		/* 739.989 Hz (fis''/ges'') */
#define Gb5 Fs5
#define G5  784		/* 783.991 Hz (g'') */
#define Gs5 831		/* 830.609 Hz (gis''/as'') */
#define Ab5 Gs5
#define A5  880		/* 880.000 Hz (a'') */
#define As5 932		/* 932.328 Hz (ais''/b'') */
#define Bb5 As5
#define B5  988		/* 987.767 Hz (h'') */
#define H5  B5

#define C6  1046	/* 1046.50 Hz (c''') */
#define Cs6 1109	/* 1108.73 Hz (cis'''/des''') */
#define Db6 Cs6
#define D6  1175	/* 1174.66 Hz (d''') */
#define Ds6 1245	/* 1244.51 Hz (dis'''/es''') */
#define Eb6 Ds6
#define E6  1319	/* 1318.51 Hz (e''') */
#define F6  1397	/* 1396.91 Hz (f''') */
#define Fs6 1480	/* 1479.98 Hz (fis'''/ges''') */
#define Gb6 Fs6
#define G6  1568	/* 1567.98 Hz (g''') */
#define Gs6 1661	/* 1661.22 Hz (gis'''/as''') */
#define Ab6 Gs6
#define A6  1760	/* 1760.00 Hz (a''') */
#define As6 1865	/* 1864.66 Hz (ais'''/b''') */
#define Bb6 As6
#define B6  1976	/* 1975.53 Hz (h''') */
#define H6  B6

#define C7  2093	/* 2093,00 Hz (c'''') */
#define Cs7 2218	/* 2217,46 Hz (cis''''/des'''') */
#define Db7 Cs7
#define D7  2349	/* 2349,32 Hz (d'''') */
#define Ds7 2489	/* 2489,02 Hz (dis''''/es'''') */
#define Eb7 Ds7
#define E7  2637	/* 2637,02 Hz (e'''') */
#define F7  2794	/* 2793,83 Hz (f'''') */
#define Fs7 2960	/* 2959,96 Hz (fis''''/ges'''') */
#define Gb7 Fs7
#define G7  3136	/* 3135,96 Hz (g'''') */
#define Gs7 3322	/* 3322,44 Hz (gis''''/as'''') */
#define Ab7 Gs7
#define A7  3520	/* 3520,00 Hz (a'''') */
#define As7 3729	/* 3729,31 Hz (ais''''/b'''') */
#define Bb7 As7
#define B7  3951	/* 3951,07 Hz (h'''') */
#define H7  B7

#define C8  4186	/* 4186,01 Hz (c''''') */

#define REST 1

#endif /* __NOTES_H__ */
