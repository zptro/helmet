#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        CalcDistribution
# Purpose:     Utilities for various calculations of different types of trip distribution models.
#               a) CalcFratar : Calculates a Fratar/IPF on a seed matrix given row and column (P and A) totals
#               b) CalcSinglyConstrained : Calculates a singly constrained trip distribution for given P/A vectors and a
#                  friction factor matrix
#               c) CalcDoublyConstrained : Calculates a doubly constrained trip distribution for given P/A vectors and a
#                  friction factor matrix (P and A should be balanced before usage, if not then A is scaled to P)
#               d) CalcMultiFratar : Applies fratar model to given set of trip matrices with multiple target production vectors and one attraction vector
#               e) CalcMultiDistribute : Applies gravity model to a given set of frication matrices with multiple production vectors and one target attraction vector
#
#              **All input vectors are expected to be numpy arrays  
#               
# Author:      Chetan Joshi, Portland OR
# Dependencies:numpy [www.numpy.org]
# Created:     5/14/2015
#              
# Copyright:   (c) Chetan Joshi 2015
# Licence:     Permission is hereby granted, free of charge, to any person obtaining a copy
#              of this software and associated documentation files (the "Software"), to deal
#              in the Software without restriction, including without limitation the rights
#              to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#              copies of the Software, and to permit persons to whom the Software is
#              furnished to do so, subject to the following conditions:
#
#              The above copyright notice and this permission notice shall be included in all
#              copies or substantial portions of the Software.
#
#              THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#              IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#              FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#              AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#              LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#              OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#              SOFTWARE.
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import numpy


def calcFratar(ProdA, AttrA, Trips1, maxIter = 10):
    '''Calculates fratar trip distribution
       ProdA = Production target as array
       AttrA = Attraction target as array
       Trips1 = Seed trip table for fratar
       maxIter (optional) = maximum iterations, default is 10
       Returns fratared trip table
    '''
    print 'Checking production, attraction balancing:'
    sumP = sum(ProdA)
    sumA = sum(AttrA)
    print 'Production: ', sumP
    print 'Attraction: ', sumA
    if sumP <> sumA:
        print 'Productions and attractions do not balance, attractions will be scaled to productions!'
        AttrA = AttrA*(sumP/sumA)
    else:
        print 'Production, attraction balancing OK.'
    #Run 2D balancing --->
    for balIter in xrange(0, maxIter):
        ComputedProductions = Trips1.sum(1)
        ComputedProductions[ComputedProductions==0]=1
        OrigFac = (ProdA/ComputedProductions)
        Trips1 = Trips1*OrigFac[:, numpy.newaxis]

        ComputedAttractions = Trips1.sum(0) 
        ComputedAttractions[ComputedAttractions==0]=1
        DestFac = (AttrA/ComputedAttractions)
        Trips1 = Trips1*DestFac
    return Trips1