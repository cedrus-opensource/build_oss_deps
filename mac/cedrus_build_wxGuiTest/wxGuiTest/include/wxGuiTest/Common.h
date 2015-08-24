///////////////////////////////////////////////////////////////////////////////
// Name:        WxGuiTest/Common.h
// Author:      Yann Rouillard, Viet Bui Xuan, Reinhold Fuereder
// Created:     2002
// Copyright:   (c) 2002 Yann Rouillard, Viet Bui Xuan, Reinhold Fuereder
// Licence:     wxWindows licence
//
// $Id: Common.h 69 2008-01-24 21:16:37Z john $
///////////////////////////////////////////////////////////////////////////////

#ifdef __WXM__
#pragma warning (disable:4018)
#pragma warning (disable:4273)
#pragma warning (disable:4284)
#pragma warning (disable:4786)
#endif

#include "wx/wxprec.h"

#ifdef __BORLANDC__
	#pragma hdrstop
#endif

#ifndef WX_PRECOMP
	#include "wx/wx.h"
#endif


#if defined(__DARWIN__) || defined( __GNUC__ )
#   ifdef WXEXPORT
#		undef WXEXPORT
#	endif
#	ifdef WXIMPORT
#		undef WXIMPORT
#	endif
#	define WXEXPORT 								__attribute__((__visibility__("default")))
#	define WXIMPORT 								// intentionally not defined.  Otherwise, implementations could wind up in the wrong library!
#endif


