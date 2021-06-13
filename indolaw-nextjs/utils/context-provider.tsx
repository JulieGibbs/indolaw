import { Context, createContext, useContext, useState, ReactNode } from 'react';
import { ColorScheme, colors, darkColors, noColors } from 'utils/theme';
import { NodeMap, Structure } from 'utils/grammar';

type AppContextType = {
  colorScheme: ColorScheme,
  invertedColorScheme: ColorScheme,
  toggleDarkMode: () => void,
};

type Props = {
  children: ReactNode,
}

const AppContext: Context<AppContextType> = createContext({
  colorScheme: noColors,
  invertedColorScheme: noColors,
  toggleDarkMode: () => { }
});

type LawContextType = {
  penjelasanMap: NodeMap,
};

export const LawContext: Context<LawContextType> = createContext({
  penjelasanMap: {},
});

export function getPenjelasanMapKey(
  structure: Structure,
  heading: string,
): string {
  return `${structure}-${heading}`;
}

export function AppContextWrapper(props: Props): JSX.Element {
  const [darkTheme, setDarkTheme] = useState(false);

  const toggleDarkMode = () => setDarkTheme(!darkTheme);
  const colorScheme = darkTheme ? darkColors : colors;
  const invertedColorScheme = darkTheme ? colors : darkColors;

  let state = {
    colorScheme,
    invertedColorScheme,
    toggleDarkMode
  }

  return (
    <AppContext.Provider value={state}>
      {props.children}
    </AppContext.Provider>
  );
}

export function useAppContext(): AppContextType {
  const context = useContext(AppContext);
  if (context.colorScheme === noColors) {
    throw Error('Component is not wrapped with a Provider?');
  }
  return context;
}
