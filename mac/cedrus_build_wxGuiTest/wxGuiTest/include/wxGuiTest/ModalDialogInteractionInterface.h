/////////////////////////////////////////////////////////////////////////////
// $RCSfile: ModalDialogInteractionInterface.h,v $
// Original Author/Owner: reinhold
//
// $Revision: 96 $ $Name:  $ $State: Exp $
//
// $Date: 2010-06-04 13:24:03 -0700 (Fri, 04 Jun 2010) $ $Author: grant $
//
//
// $Id: ModalDialogInteractionInterface.h 69 2008-01-24 21:16:37Z john $
/////////////////////////////////////////////////////////////////////////////

#ifndef MODALDIALOGINTERACTIONINTERFACE_H
#define MODALDIALOGINTERACTIONINTERFACE_H

#ifdef __GNUG__
//    #pragma interface "ModalDialogInteractionInterface.h"
#endif

namespace wxTst {


/*! \class ModalDialogInteractionInterface
    \brief Instantiations of this interface can be handed over to the
    ModalDialogTimer to be executed after the timeout.
*/
class ModalDialogInteractionInterface
{
public:
    virtual ~ModalDialogInteractionInterface() {}
    /*! \fn virtual void Execute () = 0
        \brief Manipulate, or interact with modal dialog before dismissing it.
    */
    virtual void Execute () = 0;

};

} // End namespace wxTst

#endif // MODALDIALOGINTERACTIONINTERFACE_H
