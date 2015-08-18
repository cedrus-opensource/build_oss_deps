#!/bin/bash


PATH_TO_THIS_SCRIPT=`pwd`
PATH_TO_BINARIES_DIR="${PATH_TO_THIS_SCRIPT}/../wx_binaries/"

ExportToEnvironment()
{
    export CC="clang"
    export CXX="clang++ -std=c++11 -stdlib=libc++ "
}


NUM_PARALLEL_JOBS=4

SDK_PATH="/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk"

DEPLOYMENT_TARGET="10.7"

CPPFLAGS_ARCH="-arch x86_64"

LDFLAGS_common=" -stdlib=libc++ -arch x86_64 -mmacosx-version-min=${DEPLOYMENT_TARGET} -isysroot ${SDK_PATH}  -dead_strip"

# see Viggen case 1593 regarding: -fno-strict-aliasing
CPPFLAGS_common="  -fvisibility-inlines-hidden \
-fno-strict-aliasing \
-mmacosx-version-min=${DEPLOYMENT_TARGET} \
-DMAC_OS_X_VERSION_MIN_REQUIRED=1070 \
-DMAC_OS_X_DEPLOYMENT_TARGET=1070 \
-isysroot ${SDK_PATH}"

CONFIGURE_FLAGS=" \
--enable-gui \
--disable-plugins \
--disable-monolithic \
--enable-shared \
--disable-static \
--disable-universal_binary \
--with-libpng \
--with-libjpeg \
--with-libtiff \
--with-libxpm \
--with-regex \
--with-expat \
--enable-rtti \
--enable-dnd \
--enable-controls \
--enable-dataviewctrl \
--disable-std_iostreams \
--disable-compat26 \
--disable-printfposparam \
--enable-unicode \
--enable-mediactrl \
--enable-backtrace \
--enable-catch_segvs \
--enable-fontmap \
--enable-url \
--enable-richtext \
--enable-tarstream \
--enable-zipstream \
--enable-compat28 \
--enable-utf8 \
--with-zlib \
--disable-webview-webkit \
--disable-webview \
--disable-webkit \
--without-webview \
--without-webkit "

CONFIG_FLAGS_x86=" --with-macosx-sdk=${SDK_PATH} \
--with-macosx-version-min=${DEPLOYMENT_TARGET} \
--enable-macosx_arch=x86_64 \
--without-osx_carbon \
--without-osx_iphone \
--with-osx_cocoa"



check_return_val()
{
    if [ "$1" -ne 0 ]
    then
        exit $1
    fi
}

ModifyFiles()
{
    "$PATH_TO_THIS_SCRIPT"/cedrus_wx_mach-o_dylib_fixer.sh "$PATH_TO_BINARIES_DIR"/built_libs/lib/ -v # -v # verbose
}

BuildWXDebug()
{
    CPP_DBG_FLAGS="  -g -g3 -DWXDEBUGFLAG=d "

    # NOTE: should we try  --enable-std_string_conv_in_wxstring  ?? --enable-iniconf ?
    # NOTE: #error "wxUSE_ACCESSIBILITY is currently only supported under wxMSW"

    CONF_DBG_FLAGS=" --enable-debug --enable-debug_flag --enable-debug_info --enable-debug_gdb --disable-optimise "

    mkdir -p "$PATH_TO_BINARIES_DIR"/osx-x86-debug-cg
    mkdir -p "$PATH_TO_BINARIES_DIR"/built_libs

    export WXDEBUGFLAG=d
    export CPPFLAGS="${CPP_DBG_FLAGS} ${CPPFLAGS_common} ${CPPFLAGS_ARCH}"
    export LDFLAGS="${LDFLAGS_common}"

    cd "$PATH_TO_BINARIES_DIR"/osx-x86-debug-cg

    "$PATH_TO_THIS_SCRIPT"/configure ${CONF_DBG_FLAGS} ${CONFIGURE_FLAGS} ${CONFIG_FLAGS_x86} --prefix=$PATH_TO_BINARIES_DIR/built_libs

    sed -e 's/-lwxexpat$(WXDEBUGFLAG)$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/-lwxexpat$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/' \
        -e 's/-lwxpng$(WXDEBUGFLAG)$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/-lwxpng$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/'     \
        -e 's/-lwxjpeg$(WXDEBUGFLAG)$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/-lwxjpeg$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/'   \
        -e 's/-lwxtiff$(WXDEBUGFLAG)$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/-lwxtiff$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/'   \
        -e 's/#WXDEBUGFLAG = d/WXDEBUGFLAG=d/' Makefile > CEDRUS_mac_debug_Makefile

    sed -e 's/-lwxexpat$(WXDEBUGFLAG)$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/-lwxexpat$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/' \
        -e 's/-lwxpng$(WXDEBUGFLAG)$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/-lwxpng$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/'     \
        -e 's/-lwxjpeg$(WXDEBUGFLAG)$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/-lwxjpeg$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/'   \
        -e 's/-lwxtiff$(WXDEBUGFLAG)$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/-lwxtiff$(WX_LIB_FLAVOUR)-$(WX_RELEASE)$(HOST_SUFFIX)/'   \
        -e 's/#WXDEBUGFLAG = d/WXDEBUGFLAG=d/' utils/wxrc/Makefile > utils/wxrc/CEDRUS_mac_debug_Makefile

    cp utils/wxrc/CEDRUS_mac_debug_Makefile utils/wxrc/Makefile

    make -f CEDRUS_mac_debug_Makefile -j${NUM_PARALLEL_JOBS}

    # IMPORTANT: the LAST LINE in the function BuildWXDebug must be
    # something important, not a 'cd' or an 'echo' that would ALWAYS
    # BE GUARANTEED TO SUCCEED. Do not make the last line something
    # that can trivially succeed, or that defeats the purpose of using check_return_val
    make -f CEDRUS_mac_debug_Makefile install
}

BuildWXRelease()
{
    unset WXDEBUGFLAG

    CPP_OPT_FLAGS=" -Os -g "

    # NOTE: should we try  --enable-std_string_conv_in_wxstring  ?? --enable-iniconf ?
    # NOTE: #error "wxUSE_ACCESSIBILITY is currently only supported under wxMSW"

    CONF_OPT_FLAGS=" --disable-debug --disable-debug_flag --disable-debug_info --disable-debug_gdb --enable-optimise "

    mkdir -p "$PATH_TO_BINARIES_DIR"/osx-x86-release-cg
    mkdir -p "$PATH_TO_BINARIES_DIR"/built_libs

    export CPPFLAGS="${CPP_OPT_FLAGS} ${CPPFLAGS_common} ${CPPFLAGS_ARCH}"
    export LDFLAGS="${LDFLAGS_common}"

    cd "$PATH_TO_BINARIES_DIR"/osx-x86-release-cg

    "$PATH_TO_THIS_SCRIPT"/configure ${CONF_OPT_FLAGS} ${CONFIGURE_FLAGS} ${CONFIG_FLAGS_x86} --prefix=$PATH_TO_BINARIES_DIR/built_libs

    make -j${NUM_PARALLEL_JOBS}

    make install
}


main()
{
    ExportToEnvironment

    BuildWXDebug
    check_return_val $?

    cd $PATH_TO_THIS_SCRIPT

    BuildWXRelease
    check_return_val $?

    cd $PATH_TO_THIS_SCRIPT

    ModifyFiles
    check_return_val $?
}

main $@
