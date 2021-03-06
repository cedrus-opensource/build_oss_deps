///////////////////////////////////////////////////////////////////////////////
// Name:        wxGuiTest/ProvokedWarning.h
// Author:      Reinhold Fuereder
// Created:     2004
// Copyright:   (c) 2005 Reinhold Fuereder
// Licence:     wxWindows licence
//
// $Id: ProvokedWarning.h 69 2008-01-24 21:16:37Z john $
///////////////////////////////////////////////////////////////////////////////

#ifndef PROVOKEDWARNING_H
#define PROVOKEDWARNING_H

#ifdef __GNUG__
    #pragma interface "ProvokedWarning.h"
#endif

#include <wxGuiTest/Common.h>

#include <wx/datetime.h>

namespace wxTst {


/*! \class ProvokedWarning
    \brief Holds information semi-uniquely identifying provoked/expected warnings.

    Based on the specified timeout interval provoked warnings must occur, i.e.
    pop-up within a given time span. This avoids conflicts with other provoked
    warnings issued later with overlapping or even equal caption and message
    parameters (=> semi-uniquely identification).
*/
class ProvokedWarning
{
public:
    /*! \fn ProvokedWarning (const wxString &caption, const wxString *message, const unsigned int timeout)
        \brief Constructor

        \param caption caption of provoked/expected warnings
        \param message message of provoked/expected warnings, or NULL if only
            caption should be used for convenience reasons; message is deleted
            in destructor if none-NULL
        \param timeout timeout in seconds starting during object creation
    */
    ProvokedWarning (const wxString &caption,
            const wxString& message, const unsigned int timeout);


    /*! \fn virtual ~ProvokedWarning ()
        \brief Destructor
    */
    virtual ~ProvokedWarning () {}


    /*! \fn virtual const wxString& GetCaption () const
        \brief Get caption being part of the semi-uniquely identification.

        \return caption of expected warning
    */
    virtual const wxString& GetCaption () const;


    /*! \fn virtual const wxString& GetMessage () const
        \brief Get message being part of the semi-uniquely identification.

        \return message of expected warning.
    */
    virtual const wxString& GetMessage () const;


    /*! \fn virtual const wxDateTime & GetTimeout () const
        \brief Get timeout of the provoked/expected warning.

        \return timeout of expected warning
    */
    virtual const wxDateTime& GetTimeout () const;

protected:

private:
    wxString m_caption;
    wxString m_message;
    wxDateTime m_timeout;

private:
    // No copy and assignment constructor:
    ProvokedWarning (const ProvokedWarning &rhs);
    ProvokedWarning & operator= (const ProvokedWarning &rhs);
};

} // End namespace wxTst

#endif // PROVOKEDWARNING_H

