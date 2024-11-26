/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"

//==============================================================================
/**
*/
class VacPlugin_01AudioProcessorEditor  : public juce::AudioProcessorEditor
{
public:
    VacPlugin_01AudioProcessorEditor (VacPlugin_01AudioProcessor&);
    ~VacPlugin_01AudioProcessorEditor() override;

    //==============================================================================
    void paint (juce::Graphics&) override;
    void resized() override;

private:
    // This reference is provided as a quick way for your editor to
    // access the processor object that created it.
    VacPlugin_01AudioProcessor& audioProcessor;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (VacPlugin_01AudioProcessorEditor)
};
