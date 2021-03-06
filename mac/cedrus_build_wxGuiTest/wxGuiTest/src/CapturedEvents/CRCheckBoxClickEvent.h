///////////////////////////////////////////////////////////////////////////////
// Name:        wxGuiTest/CapturedEvents/CRCheckBoxClickEvent.h
// Author:      Reinhold Fuereder
// Created:     2004
// Copyright:   (c) 2005 Reinhold Fuereder
// Modifications: John Ralls, 2007-2008
// Modifications Copyright: (c) 2008 John Ralls
// Licence:     wxWindows licence
//
// $Id: CRCheckBoxClickEvent.h 69 2008-01-24 21:16:37Z john $
///////////////////////////////////////////////////////////////////////////////

#ifndef SWCRCHECKBOXCLICKEVENT_H
#define SWCRCHECKBOXCLICKEVENT_H

#ifdef __GNUG__
    #pragma interface "CRCheckBoxClickEvent.h"
#endif

#include <wxGuiTest/Common.h>

#include "CRCapturedEvent.h"

namespace wxTst {


/*! \class CRCheckBoxClickEvent
    \brief Handle check box click events.
*/
class CRCheckBoxClickEvent : public CRCapturedEvent
{
public:
    /*! \fn CRCheckBoxClickEvent (wxEvent *event)
        \brief Constructor

        \param event event to handle
    */
    CRCheckBoxClickEvent (wxEvent *event);


    /*! \fn virtual ~CRCheckBoxClickEvent ()
        \brief Destructor
    */
    virtual ~CRCheckBoxClickEvent ();


    /*! \fn virtual void Process (CRCapturedEvent **pendingEvt)
        \brief Process event, only called after checking for handling ability.
    
        \param pendingEvt current pending event with respect to code emitting
            (or NULL if none is pending)
    */
    virtual void Process (CRCapturedEvent **pendingEvt);


    /*! \fn virtual void EmitCpp ()
        \brief Emit event simulation specific C++ code.
    */
    virtual void EmitCpp ();

protected:

private:
    wxString m_containerName;
    wxString m_checkBoxName;
    bool m_isChecked;

private:
    // No copy and assignment constructor:
    CRCheckBoxClickEvent (const CRCheckBoxClickEvent &rhs);
    CRCheckBoxClickEvent & operator= (const CRCheckBoxClickEvent &rhs);
};

} // End namespace wxTst

#endif // SWCRCHECKBOXCLICKEVENT_H

