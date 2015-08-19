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


export BOOST_VERSION="1_50"
export BOOST_VERSION_NAME="boost_${BOOST_VERSION}_0"

export BOOST="`pwd`/../binaries_boost"

export BJAM_FLAGS=" toolset=clang-11 --build-type=complete --layout=versioned threading=multi link=shared runtime-link=shared release install "
export WITH_WHICH_LIBS=" --with-chrono --with-date_time --with-filesystem --with-iostreams  --with-math  --with-regex --with-serialization --with-signals --with-system --with-thread --with-program_options "
export BOOTSTRAP_LIBS=" --with-libraries=chrono,date_time,filesystem,iostreams,math,regex,serialization,signals,system,thread,program_options "

DEST_DIR="$BOOST"/lib

PATH_TO_THIS_SCRIPT=`pwd`

check_return_val()
{
    if [ "$1" -ne 0 ]; then
        exit $1;
    fi
}

BuildBoost()
{
    for VERS in "$@"
    do
        echo "--- Building and installing ${VERS} ---"

        ./bootstrap.sh  --with-python=/Library/Frameworks/Python.framework/Versions/2.6/bin/python  --with-python-root=/Library/Frameworks/Python.framework/Versions/2.6 ${BOOTSTRAP_LIBS}

        check_return_val $?

        BJAM_FLAGS="-j`sysctl hw.ncpu | awk '// {print $2*1.5}'`  address-model=64 macosx-version=10.7  macosx-version-min=10.7 --build-dir=bin/mac10_7/ --prefix=out/install ${BJAM_FLAGS} ${WITH_WHICH_LIBS} "

        echo "Executing ./bjam ${BJAM_FLAGS}"
        ./bjam ${BJAM_FLAGS}

        check_return_val $?

    done
}


RunDsymUtil()
{
    for FILE in `ls "$DEST_DIR"/*.dylib`
    do
        NAME=`basename "$FILE"`

        if [ \( ! -h "$DEST_DIR"/"$NAME" \) -a "$DEST_DIR"/"$NAME" -nt "$DEST_DIR"/"$NAME".dSYM ]
        then
            # Since we're stripping the dylib afterwards, it's critical that
            # this not get run on a stripped library.

            echo "     Creating DWARF with dSYM for $NAME"
            if dsymutil "$DEST_DIR"/"$NAME" --out="$DEST_DIR"/"$NAME".dSYM
            then
                echo "        Stripping $NAME"
                strip -u -r -S "$DEST_DIR"/"$NAME"
            fi
        fi
    done
}


ModifyFiles()
{
    for LIB in "$DEST_DIR"/libboost*mt-*.dylib
    do
        LIBNAME=`basename "$LIB"`
        OLDNAME=`otool -D "$LIB" | tail -1`
        if [[ "$OLDNAME" != @executable_path/$LIBNAME ]]
        then
            echo "--- Updating references to $LIBNAME ---"
            for FILE in "$DEST_DIR"/libboost*mt-*.dylib
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
    BuildBoost $BOOST_VERSION_NAME

    ModifyFiles  # calls to install_name_tool and otool

    RunDsymUtil

    exit $?
}

main $@
