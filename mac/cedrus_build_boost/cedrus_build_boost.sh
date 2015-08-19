#!/bin/bash

#The (in-use-by-cedrus) Boost libraries requiring separate building and installation are:

#    - chrono
#    - date_time
#    - filesystem
#    - iostreams
#    - locale
#    - math
#    - python
#    - regex
#    - serialization
#    - signals
#    - system
#    - thread
#    - program_options


BOOST_BINARIES_DIR="`pwd`/../binaries_boost/install"

LIBS_DEST_DIR="$BOOST_BINARIES_DIR"/lib

PATH_TO_THIS_SCRIPT=`pwd`

WITH_WHICH_LIBS=" --with-chrono \
--with-date_time \
--with-filesystem \
--with-iostreams  \
--with-math \
--with-regex \
--with-serialization \
--with-signals \
--with-system \
--with-thread \
--with-program_options "

B2_FLAGS=" -j6 \
cxxflags='-stdlib=libc++' \
cxxflags='-std=c++11' \
linkflags='-stdlib=libc++' \
--prefix=${BOOST_BINARIES_DIR} \
--includedir=${BOOST_BINARIES_DIR}/include \
--layout=versioned \
toolset=clang-11 \
variant=release \
link=shared \
threading=multi \
runtime-link=shared \
address-model=64 \
macosx-version=10.7 \
macosx-version-min=10.7 \
--build-dir=bin/mac10_7/ \
${WITH_WHICH_LIBS} \
install "


# (note from Aug 2015) The next time we build pyLSClient, we probably need to change the '--with-python' option to 2.7
BOOTSTRAP_LIBS=" --with-libraries=chrono,date_time,filesystem,iostreams,math,regex,serialization,signals,system,thread,program_options \
--with-python=/Library/Frameworks/Python.framework/Versions/2.6/bin/python \
--with-python-root=/Library/Frameworks/Python.framework/Versions/2.6 "


check_return_val()
{
    if [ "$1" -ne 0 ]; then
        exit $1;
    fi
}

BuildBoost()
{
    ./bootstrap.sh ${BOOTSTRAP_LIBS}

    check_return_val $?

    # necessary step for building 'modular boost' (official name for 'building from the boost git repo')
    ./b2 headers

    # compile the binary libraries:
    echo "Executing ./b2 ${B2_FLAGS}"
    ./b2 ${B2_FLAGS}

    check_return_val $?
}


RunDsymUtil()
{
    for FILE in `ls "$LIBS_DEST_DIR"/*.dylib`
    do
        NAME=`basename "$FILE"`

        if [ \( ! -h "$LIBS_DEST_DIR"/"$NAME" \) -a "$LIBS_DEST_DIR"/"$NAME" -nt "$LIBS_DEST_DIR"/"$NAME".dSYM ]
        then
            # Since we're stripping the dylib afterwards, it's critical that
            # this not get run on a stripped library.

            echo "     Creating DWARF with dSYM for $NAME"
            if dsymutil "$LIBS_DEST_DIR"/"$NAME" --out="$LIBS_DEST_DIR"/"$NAME".dSYM
            then
                echo "        Stripping $NAME"
                strip -u -r -S "$LIBS_DEST_DIR"/"$NAME"
            fi
        fi
    done
}


ModifyFiles()
{
    for LIB in "$LIBS_DEST_DIR"/libboost*mt-*.dylib
    do
        LIBNAME=`basename "$LIB"`
        OLDNAME=`otool -D "$LIB" | tail -1`
        if [[ "$OLDNAME" != @executable_path/$LIBNAME ]]
        then
            echo "--- Updating references to $LIBNAME ---"
            for FILE in "$LIBS_DEST_DIR"/libboost*mt-*.dylib
            do
                if [ -n "`otool -L ${FILE} | grep ${OLDNAME} | grep version`" ]
                then
                    echo "    Updating `basename $FILE` to link to @executable_path/$LIBNAME"
                    install_name_tool -change "$OLDNAME" @executable_path/$LIBNAME "$FILE"
                fi
            done
            install_name_tool -id @executable_path/$LIBNAME "$LIB"
        fi
    done
}



main()
{
    BuildBoost

    ModifyFiles  # calls to install_name_tool and otool

    RunDsymUtil

    exit $?
}

main $@
