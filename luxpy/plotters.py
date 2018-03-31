# -*- coding: utf-8 -*-
"""
###################################################################################################
# Module with functions related to plotting 
###################################################################################################
#
# plot_color_data(): Plot color data (local helper function)
#
# plotDL(): Plot daylight locus. 
#
# plotBB(): Plot blackbody locus. 
#
# plotSL(): Plot spectrum locus.  (plotBB() and plotDL() are also called, but can be turned off).
#
# plotcerulean(): Plot cerulean (yellow (577 nm) - blue (472 nm)) line (Kuehni, CRA, 2013: Table II: spectral lights) [Kuehni, R. G. (n.d.). Unique hues and their stimuli—state of the art. Color Research & Application, 39(3), 279–287](https://doi.org/10.1002/col.21793)
#
# plotUH(): Plot unique hue lines from color space center point xyz0. (Kuehni, CRA, 2013: uY,uB,uG: Table II: spectral lights; uR: Table IV: Xiao data) [Kuehni, R. G. (n.d.). Unique hues and their stimuli—state of the art. Color Research & Application, 39(3), 279–287](https://doi.org/10.1002/col.21793)
#
#--------------------------------------------------------------------------------------------------

Created on Tue Jul  4 14:44:45 2017

@author: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""

from luxpy import *
import matplotlib.pyplot as plt 
__all__ = ['plotSL','plotDL','plotBB','plot_color_data','plotceruleanline','plotUH']



def plot_color_data(x,y,z=None, axh=None, show = True, cieobs =_CIEOBS, cspace = _CSPACE,  formatstr = 'k-', **kwargs):
    """
    Plot color data from x,y [,z].
    
    Args: 
        :x: float or numpy.ndarray with x-coordinate data
        :y: float or numpy.ndarray with y-coordinate data
        :z: None or float or numpy.ndarray with Z-coordinate data, optional
            If None: make 2d plot.
        :axh: None or axes handle, optional
            Determines axes to plot data in.
            None: make new figure.
        :show: True or False, optional
            Invoke matplotlib.pyplot.show() right after plotting
        :cieobs: luxpy._CIEOBS or str, optional
            Determines CMF set to calculate spectrum locus or other.
        :cspace: luxpy._CSPACE or str, optional
            Determines color space / chromaticity diagram to plot data in.
            Note that data is expected to be in specified :cspace:
        :formatstr: 'k-' or str, optional
            Format str for plotting (see ?matplotlib.pyplot.plot)
        :**kwargs: additional keyword arguments for use with matplotlib.pyplot.
    
    Returns:
        :returns: None (:show: == True) or handle to current axes (:show: == False)
    """

    if 'grid' in kwargs.keys():
        plt.grid(kwargs['grid']);kwargs.pop('grid')
    if z is not None:
        plt.plot(x,y,z,formatstr, linewidth = 2)
        plt.xlabel(_CSPACE_axes[cspace][0], kwargs)
    else:
        plt.plot(x,y,formatstr,linewidth = 2)
        
    plt.xlabel(_CSPACE_axes[cspace][1], kwargs)
    plt.ylabel(_CSPACE_axes[cspace][2], kwargs)

    if show == True:
        plt.show()
    else:
        return plt.gca()



def plotDL(ccts = None, cieobs =_CIEOBS, cspace = _CSPACE, axh = None, show = True, force_daylight_below4000K = False, cspace_pars = {}, formatstr = 'k-',  **kwargs):
    """
    Plot daylight locus.
    
    Args: 
        :ccts: None or list{float], optional
            None defaults to [4000 K to 1e19 K] in 100 steps on a log10 scale.
        :force_daylight_below4000K: False or True, optional
            CIE daylight phases are not defined below 4000 K. If True plot anyway.
        :axh: None or axes handle, optional
            Determines axes to plot data in.
            None: make new figure.
        :show: True or False, optional
            Invoke matplotlib.pyplot.show() right after plotting
        :cieobs: luxpy._CIEOBS or str, optional
            Determines CMF set to calculate spectrum locus or other.
        :cspace: luxpy._CSPACE or str, optional
            Determines color space / chromaticity diagram to plot data in.
            Note that data is expected to be in specified :cspace:
        :formatstr: 'k-' or str, optional
            Format str for plotting (see ?matplotlib.pyplot.plot)
        :cspace_pars: {} or dict, optional
            Dict with parameters required by color space specified in :cspace: (for use with luxpy.colortf())
        :**kwargs: additional keyword arguments for use with matplotlib.pyplot.
    
    Returns:
        :returns: None (:show: == True) or handle to current axes (:show: == False)
    """
    
    if ccts is None:
        ccts = 10**np.linspace(np.log10(4000.0),np.log10(10.0**19.0),100.0)
        
    xD,yD = daylightlocus(ccts, force_daylight_below4000K = force_daylight_below4000K)
    Y = 100*np.ones(xD.shape)
    DL =  Yxy_to_xyz(np.vstack((Y, xD,yD)).T)
    DL = colortf(DL, tf = cspace, tfa0 = cspace_pars)
    Y,x,y = asplit(DL)
    
    axh = plot_color_data(x,y,axh = axh, cieobs = cieobs, cspace = cspace, show=show, formatstr=formatstr, **kwargs)    
    
    if show == False:
        return axh
    
def plotBB(ccts = None, cieobs =_CIEOBS, cspace = _CSPACE, axh = None, cctlabels = True, show = True, cspace_pars = {}, formatstr = 'k-',  **kwargs):  
    """
    Plot blackbody locus.
        
    Args: 
        :ccts: None or list{float], optional
            None defaults to [1000 to 1e19 K].
            Range: [1000.0,1500.0,2000.0,2500.0,3000.0,3500.0,4000.0,5000.0,6000.0,8000.0,10000.0] + [15000 K to 1e19 K] in 100 steps on a log10 scale
        :cctlabels: True or False, optional
            Add cct text labels at various points along the blackbody locus.
        :axh: None or axes handle, optional
            Determines axes to plot data in.
            None: make new figure.
        :show: True or False, optional
            Invoke matplotlib.pyplot.show() right after plotting
        :cieobs: luxpy._CIEOBS or str, optional
            Determines CMF set to calculate spectrum locus or other.
        :cspace: luxpy._CSPACE or str, optional
            Determines color space / chromaticity diagram to plot data in.
            Note that data is expected to be in specified :cspace:
        :formatstr: 'k-' or str, optional
            Format str for plotting (see ?matplotlib.pyplot.plot)
        :cspace_pars: {} or dict, optional
            Dict with parameters required by color space specified in :cspace: (for use with luxpy.colortf())
        :**kwargs: additional keyword arguments for use with matplotlib.pyplot.
    
    Returns:
        :returns: None (:show: == True) or handle to current axes (:show: == False)
    """
    if ccts is None:
        ccts1 = np.array([1000.0,1500.0,2000.0,2500.0,3000.0,3500.0,4000.0,5000.0,6000.0,8000.0,10000.0])
        ccts2 = 10**np.linspace(np.log10(15000.0),np.log10(10.0**19.0),100.0)
        ccts = np.hstack((ccts1,ccts2))
    else:
        ccts1 = None
    
    BB = cri_ref(ccts,ref_type='BB')
    xyz = spd_to_xyz(BB,cieobs = cieobs)
    Yxy = colortf(xyz, tf = cspace, tfa0 = cspace_pars)
    Y,x,y = asplit(Yxy)
   
    axh = plot_color_data(x,y,axh = axh, cieobs = cieobs, cspace = cspace, show=show, formatstr=formatstr, **kwargs)    

    if (cctlabels == True) & (ccts1 is not None):
        for i in range(ccts1.shape[0]):
            if ccts1[i]>= 3000.0:
                if i%2 == 0.0:
                    plt.plot(x[i],y[i],'k+', color = '0.5')
                    plt.text(x[i]*1.05,y[i]*0.95,'{:1.0f}K'.format(ccts1[i]), color = '0.5')
        plt.plot(x[-1],y[-1],'k+', color = '0.5')
        plt.text(x[-1]*1.05,y[-1]*0.95,'{:1.3e}K'.format(ccts[-1]), color = '0.5')    
    if show == False:
        return axh
    
def plotSL(cieobs =_CIEOBS, cspace = _CSPACE,  DL = True, BBL = True, D65 = False, EEW = False, cctlabels = False, axh = None, show = True, cspace_pars = {}, formatstr = 'k-', **kwargs):
    """
    Plot spectrum locus for cieobs in cspace.
    
    Args: 
        :DL: True or False, optional
            True plots Daylight Locus as well.
        :BBL: True or False, optional
            True plots BlackBody Locus as well. 
        :D65: False or True, optional
            True plots D65 chromaticity as well. 
        :EEW: False or True, optional
            True plots Equi-Energy-White chromaticity as well. 
        :cctlabels: False or True, optional
            Add cct text labels at various points along the blackbody locus.
        :axh: None or axes handle, optional
            Determines axes to plot data in.
            None: make new figure.
        :show: True or False, optional
            Invoke matplotlib.pyplot.show() right after plotting
        :cieobs: luxpy._CIEOBS or str, optional
            Determines CMF set to calculate spectrum locus or other.
        :cspace: luxpy._CSPACE or str, optional
            Determines color space / chromaticity diagram to plot data in.
            Note that data is expected to be in specified :cspace:
        :formatstr: 'k-' or str, optional
            Format str for plotting (see ?matplotlib.pyplot.plot)
        :cspace_pars: {} or dict, optional
            Dict with parameters required by color space specified in :cspace: (for use with luxpy.colortf())
        :**kwargs: additional keyword arguments for use with matplotlib.pyplot.
    
    Returns:
        :returns: None (:show: == True) or handle to current axes (:show: == False)
    """
    SL = _CMF['bar'][cieobs][1:4].T
    SL = np.vstack((SL,SL[0]))
    SL = 100.0*SL/SL[:,1,None]
    SL = colortf(SL, tf = cspace, tfa0 = cspace_pars)
    Y,x,y = asplit(SL)
    
    showcopy = show.copy()
    if np.any([DL,BBL,D65,EEW]):
        show = False

        
    axh_ = plot_color_data(x,y,axh = axh, cieobs = cieobs, cspace = cspace, show = show, formatstr=formatstr,  **kwargs)
    
    if DL == True:
        plotDL(ccts = None, cieobs = cieobs, cspace = cspace, axh = axh, show = show, cspace_pars = cspace_pars, formatstr = 'b:',  **kwargs)
    if BBL == True:
        plotBB(ccts = None, cieobs = cieobs, cspace = cspace, axh = axh, show = show, cspace_pars = cspace_pars, cctlabels = cctlabels, formatstr = 'r-.',  **kwargs)
    
    if D65 == True:
        YxyD65 = colortf(spd_to_xyz(_CIE_ILLUMINANTS['D65']), tf = cspace, tfa0 = cspace_pars)
        plt.plot(YxyD65[...,1],YxyD65[...,2],'bo')
    if EEW == True:
        YxyEEW = colortf(spd_to_xyz(_CIE_ILLUMINANTS['E']), tf = cspace, tfa0 = cspace_pars)
        plt.plot(YxyEEW[...,1],YxyEEW[...,2],'ko')
        
    if showcopy == False:
        return axh_
    else:
        plt.show()
        
        
def plotceruleanline(cieobs = _CIEOBS, cspace = _CSPACE, axh = None,formatstr = 'ko-', cspace_pars = {}):
    """
    Plot cerulean (yellow (577 nm) - blue (472 nm)) line (Kuehni, CRA, 2013: Table II: spectral lights).
    
    Args: 
        :axh: None or axes handle, optional
            Determines axes to plot data in.
            None: make new figure.
        :cieobs: luxpy._CIEOBS or str, optional
            Determines CMF set to calculate spectrum locus or other.
        :cspace: luxpy._CSPACE or str, optional
            Determines color space / chromaticity diagram to plot data in.
            Note that data is expected to be in specified :cspace:
        :formatstr: 'k-' or str, optional
            Format str for plotting (see ?matplotlib.pyplot.plot)
        :cspace_pars: {} or dict, optional
            Dict with parameters required by color space specified in :cspace: (for use with luxpy.colortf())
        :**kwargs: additional keyword arguments for use with matplotlib.pyplot.
    
    Returns:
        :returns: handle to cerulean line
        
    References:
        ..[1] Kuehni, R. G. (2014). Unique hues and their stimuli—state of the art. 
                Color Research & Application, 39(3), 279–287. 
                https://doi.org/10.1002/col.21793
                (see Table II, IV)
    """
    cmf = _CMF['bar'][cieobs]
    p_y = cmf[0] == 577.0 #Kuehni, CRA 2013 (mean, table IV)
    p_b = cmf[0] == 472.0 #Kuehni, CRA 2013 (mean, table IV)
    xyz_y = cmf[1:,p_y].T
    xyz_b = cmf[1:,p_b].T
    lab = colortf(np.vstack((xyz_b,xyz_y)),tf = cspace, tfa0 = cspace_pars)
    if axh is None:
        axh = plt.gca()
    hcerline = axh.plot(lab[:,1],lab[:,2],formatstr,label = 'Cerulean line')    
    return hcerline

    
def plotUH(xyz0 = None, uhues = [0,1,2,3], cieobs = _CIEOBS, cspace = _CSPACE, axh = None,formatstr = ['yo-.','bo-.','ro-.','go-.'], excludefromlegend = '',cspace_pars = {}):
    """ 
    Plot unique hue lines from color space center point xyz0.
    
    Kuehni, CRA, 2014: uY,uB,uG: Table II: spectral lights; uR: Table IV: Xiao data.
    
    Args: 
        :xyz0: None, optional
            Center of color space (unique hue lines are expected to cross here)
            None defaults to equi-energy-white.
        :uhues: [0,1,2,3], optional
            Unique hue lines to plot [0: 'yellow',1: 'blue',2: 'red',3: 'green']
        :axh: None or axes handle, optional
            Determines axes to plot data in.
            None: make new figure.
        :cieobs: luxpy._CIEOBS or str, optional
            Determines CMF set to calculate spectrum locus or other.
        :cspace: luxpy._CSPACE or str, optional
            Determines color space / chromaticity diagram to plot data in.
            Note that data is expected to be in specified :cspace:
        :formatstr: ['yo-.','bo-.','ro-.','go-.'] or list[str], optional
            Format str for plotting the different unique lines (see also ?matplotlib.pyplot.plot)
        :excludefromlegend: '' or str, optional
            To exclude certain hues from axes legend.
        :cspace_pars: {} or dict, optional
            Dict with parameters required by color space specified in :cspace: (for use with luxpy.colortf())
          
    Returns:
        :returns: list[handles] to unique hue lines
        
    References:
        ..[1] Kuehni, R. G. (2014). Unique hues and their stimuli—state of the art. 
                Color Research & Application, 39(3), 279–287. 
                https://doi.org/10.1002/col.21793
                (see Table II, IV)
    """
    hues = ['yellow','blue','red','green']
    cmf = _CMF['bar'][cieobs]
    p_y = cmf[0] == 577.0 #unique yellow,#Kuehni, CRA 2013 (mean, table IV: spectral data)
    p_b = cmf[0] == 472.0 #unique blue,Kuehni, CRA 2013 (mean, table IV: spectral data)
    p_g = cmf[0] == 514.0 #unique green, Kuehni, CRA 2013 (mean, table II: spectral data)
    p_r = cmf[0] == 650.0 #unique red, Kuehni, CRA 2013 (Xiao data, table IV: display data)
    xyz_y = 100.0*cmf[1:,p_y].T
    xyz_b = 100.0*cmf[1:,p_b].T
    xyz_g = 100.0*cmf[1:,p_g].T
    xyz_r = 100.0*cmf[1:,p_r].T
    xyz_uh = np.vstack((xyz_y,xyz_b,xyz_r,xyz_g))
    huniquehues = []
    if xyz0 is None:
        xyz0 = np.array([100.0,100.0,100.0])
    if axh is None:
        axh = plt.gca()
    for huenr in uhues:
        lab = colortf(np.vstack((xyz0,xyz_uh[huenr])),tf = cspace, tfa0 = cspace_pars)
        huh = axh.plot(lab[:,1],lab[:,2],formatstr[huenr],label = excludefromlegend + 'Unique '+ hues[huenr])
        huniquehues = [huniquehues,huh]
    return  huniquehues