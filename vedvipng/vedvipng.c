/* dvipng.c */

/************************************************************************

  visualequation is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  visualequation is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.

  This file incorporates work covered by the following copyright and
  permission notice:

        Part of the dvipng distribution

  		This program is free software: you can redistribute it and/or modify
  		it under the terms of the GNU Lesser General Public License as
  		published by the Free Software Foundation, either version 3 of the
  		License, or (at your option) any later version.

  		This program is distributed in the hope that it will be useful, but
  		WITHOUT ANY WARRANTY; without even the implied warranty of
  		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  		Lesser General Public License for more details.

  		You should have received a copy of the GNU Lesser General Public
  		License along with this program. If not, see
  		<http://www.gnu.org/licenses/>.

  		Copyright (C) 2002-2015 Jan-�ke Larsson

************************************************************************/

/* This program translates TeX's DVI-Code into Portable Network Graphics. */

#define MAIN
#include "vedvipng.h"

#ifdef MIKTEX
#  define main __cdecl Main
#endif        /* MIKTEX */
/**********************************************************************/
/*******************************  main  *******************************/
/**********************************************************************/
int vedvipng(int vedpi, int output_length, int output[][4])
{
	if (vedvipngpath == NULL || veinputfile == NULL || veoutputfile == NULL) {
	    fflush(stdout);
	    fprintf(stderr, "vedvipng.so: VE parameters are not set.");
		exit(EXIT_FATAL);
	}
	veN = output_length;
	vep = &output;
	/*bool parsestdin;*/

#ifdef TIMING
# ifdef HAVE_GETTIMEOFDAY
  gettimeofday(&Tp, NULL);
  timer = Tp.tv_sec + Tp.tv_usec / 1000000.0;
# else
#  ifdef HAVE_FTIME
  ftime(&timebuffer);
  timer = timebuffer.time + timebuffer.millitm / 1000.0;
#  endif
# endif
#endif
  /* setbuf(stderr, NULL); */

#ifdef HAVE_LIBKPATHSEA
  kpse_set_program_name(vedvipngpath, "dvips");
  /* Use extra paths as used by dvips */
  /* kpse_set_program_name(argv[0],"dvips");  Commented for Visual Equation */
  /* If dvipng is not installed in the texmf tree, and _only_
   * SELFAUTO...  is used in texmf.cnf, kpathsea will not find a)
   * Virtual fonts b) ps2pk.map or psfonts.map c) PostScript fonts
   *
   * We adjust these things here
   */
  /* char selfautodir[MAXPATHLEN];
     FILE *self;
     self = popen("kpsewhich -expand-var='$SELFAUTODIR'", "r");
     if (!self)
       ...
     if (!fgets(selfautodir, MAXPATHLEN, self))
       ...
    fclose(self); */
# ifdef ENV_SELFAUTOLOC
  putenv(ENV_SELFAUTOLOC);
# endif
# ifdef ENV_SELFAUTODIR
  putenv(ENV_SELFAUTODIR);
# endif
# ifdef ENV_SELFAUTOPARENT
  putenv(ENV_SELFAUTOPARENT);
# endif
  kpse_set_program_enabled (kpse_pk_format, makeTexPK, kpse_src_compile);
#endif

#ifdef HAVE_TEXLIVE_GS_INIT
  texlive_gs_init();
#endif

	initcolor();
	/* parsestdin = DecodeArgs(argc, argv); */

	/* Settings options used by Visual Equation */
	option_flags &= ~BE_NONQUIET;
	option_flags |= VE_OUTPUT;
	/* -T tight */
	x_width_def=-1;
	y_width_def=-1;
	/* -D dpi */
	dpi = vedpi;
	/* --follow */
	DVIFollowToggle();
	/* -o output AND input */
	dvi = DVIOpen (veinputfile, veoutputfile);
	ParsePages("-");

#ifdef HAVE_LIBKPATHSEA
	/* Commented for Visual Equation
  if (user_mfmode)
    if (user_bdpi)
      kpse_init_prog("VEDVIPNG", user_bdpi, user_mfmode, "cmr10");
    else {
      Warning("--mfmode given without --bdpi");
      // this will give a lot of warnings but...
      kpse_init_prog("VEDVIPNG", 300, user_mfmode, "cmr10");
    }
  else */
    kpse_init_prog("VEDVIPNG", 300, "cx", "cmr10");
#endif

#ifdef HAVE_FT2
  InitPSFontMap();
#endif

  if (dvi!=NULL) DrawPages();

  /* Commented for Visual Equation
  if (parsestdin) {
    char    line[STRSIZE];

    printf("%s> ",dvi!=NULL?dvi->name:"");
    while(fgets(line,STRSIZE,stdin)) {
      DecodeString(line);
      if (dvi!=NULL) {
	DVIReOpen(dvi);
	DrawPages();
      }
      printf("%s> ",dvi!=NULL?dvi->name:"");
    }
    printf("\n");
  }*/

#ifdef TIMING
# ifdef HAVE_GETTIMEOFDAY
  gettimeofday(&Tp, NULL);
  timer = Tp.tv_sec + Tp.tv_usec/1000000.0 - timer;
# else
#  ifdef HAVE_FTIME
  ftime(&timebuffer);
  timer = timebuffer.time + timebuffer.millitm/1000.0 - timer;
#  endif
# endif

  if (ndone > 0)
    fprintf(stderr,
	    "Time of complete run: %.2f s, %d page(s), %.4f s/page.\n",
	    timer, ndone, timer / ndone);
  if (my_toc >= 0.0001)
    fprintf(stderr,
	    "Thereof in TIC/TOC region %.5f s.\n",my_toc);
#endif

  ClearFonts();
  DVIClose(dvi);
  /* Fix for Visual Equation */
  dvi = NULL;
  /* Unneeded, but it does not harm.*/
  vep = NULL; veN = -1;

  ClearColorNames();
#ifdef HAVE_FT2
  ClearPSFontMap();
  ClearEncoding();
  ClearSubfont();
  if (libfreetype!=NULL && FT_Done_FreeType(libfreetype))
    Fatal("an error occurred during freetype destruction");
  libfreetype = NULL;
#endif

  /* exit(exitcode);*/
  return 0;
}
